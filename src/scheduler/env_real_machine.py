"""
量子任务调度环境的真机闭环模块
Real-Machine Closed-Loop for Quantum-Classical Hybrid Task Scheduling Environment

本模块封装真机闭环的核心逻辑（Issue #64），将依赖环境内部状态的
方法抽离为独立函数，便于单测与复用：
    - submit_to_real_machine   : 向真机非阻塞提交一个量子任务
    - record_real_failure      : 记录一次真机失败并在阈值时触发降级
    - poll_pending_real_tasks  : 非阻塞轮询已提交真机任务的结果

依赖关系：仅依赖 env_types.py 中的常量与数据类，不依赖 env.py。
真机函数通过 ``env`` 参数访问环境内部状态（如 _pending_real_tasks、
_real_clients 等），从而避免循环导入。
"""

from typing import TYPE_CHECKING, Any

from loguru import logger

from src.scheduler.env_types import (
    REAL_MACHINE_DEGRADE_FAIL_THRESHOLD,
    REAL_MACHINE_FAIL_PENALTY,
    REAL_MACHINE_MAX_POLL_STEPS,
    REAL_MACHINE_SUCCESS_BONUS,
    QuantumMachine,
    Task,
)

if TYPE_CHECKING:
    # 仅用于类型标注，避免运行时循环导入
    from src.scheduler.env import QuantumSchedulingEnv


def submit_to_real_machine(
    env: "QuantumSchedulingEnv",
    machine: QuantumMachine,
    task: Task,
) -> None:
    """
    向真机提交一个量子任务（非阻塞，异常安全）。

    真机提交在仿真循环中是非阻塞的：提交后立即返回 task_id 并登记到
    ``env._pending_real_tasks``，后续 step() 通过 ``poll_pending_real_tasks``
    轮询结果，避免阻塞 RL 训练。

    降级机制（Issue #64）：当 ``env._real_machine_degraded=True`` 时跳过提交，
    真机不可用时自动 fallback 到 Mock（仅计入仿真统计）。

    Args:
        env     : 调度环境实例（提供真机客户端、pending 列表等内部状态）
        machine : 目标真机
        task    : 待提交任务
    """
    # 降级保护：已知真机不可用时直接返回，不再消耗机时
    if env._real_machine_degraded:
        return

    client = env._real_clients.get(machine.name)
    if client is None:
        return
    # 构造一个最小可执行的 QCIS 电路（H 门 + 测量），用于真机验证
    # 真实场景下应由 parser 从 task 生成 QCIS，这里用占位电路做连通性验证
    qcis = getattr(task, "qcis", None) or "H Q0\nM Q0"
    try:
        real_task_id = client.submit_quantum_task(
            qcis=qcis,
            shots=512,
            task_name=f"RL_{task.task_id}",
        )
        env._machine_real_submits[machine.name] = (
            env._machine_real_submits.get(machine.name, 0) + 1
        )
        # 登记到 pending 列表，后续轮询结果（Issue #64）
        # real_task_id 为 None 表示提交被拒绝（如机器校准中），计入失败
        if real_task_id is not None:
            env._pending_real_tasks.append(
                {
                    "task_id": str(real_task_id),
                    "machine_name": machine.name,
                    "submit_step": env._current_step,
                    "poll_count": 0,
                    "task_id_str": str(task.task_id),
                }
            )
            if env.use_real_machine:
                logger.debug(
                    f"[真机闭环] 任务 {task.task_id} 已提交 {machine.name} "
                    f"(real_task_id={real_task_id})，等待结果轮询"
                )
        else:
            # 提交被拒绝（非异常），计入失败并触发降级判断
            record_real_failure(env, machine.name, "提交被拒绝（返回 None）")
    except Exception as e:
        # 真机 API 提交可能因网络/认证/服务端等多种原因失败，无法精确收窄
        logger.error(f"[真机] {machine.name} 提交失败: {e}")
        env._render_log.append(f"[真机] {machine.name} 提交失败: {str(e)[:60]}")
        record_real_failure(env, machine.name, f"提交异常: {str(e)[:60]}")


def record_real_failure(
    env: "QuantumSchedulingEnv",
    machine_name: str,
    reason: str,
) -> None:
    """
    记录一次真机失败，并在达到阈值时触发降级（Issue #64）。

    连续失败次数达到 ``REAL_MACHINE_DEGRADE_FAIL_THRESHOLD`` 时，将
    ``env._real_machine_degraded`` 置为 True，后续真机提交将被跳过。

    Args:
        env          : 调度环境实例
        machine_name : 失败的机器名
        reason       : 失败原因（用于日志）
    """
    env._real_fail_count += 1
    env._real_consecutive_failures += 1
    if (
        env._real_consecutive_failures >= REAL_MACHINE_DEGRADE_FAIL_THRESHOLD
        and not env._real_machine_degraded
    ):
        env._real_machine_degraded = True
        logger.warning(
            f"[真机闭环] 连续失败 {env._real_consecutive_failures} 次，"
            f"已自动降级到 Mock 模式（最后失败: {machine_name} - {reason}）"
        )
        env._render_log.append(
            f"[真机闭环] 已降级到 Mock（连续失败 {env._real_consecutive_failures} 次）"
        )


def poll_pending_real_tasks(env: "QuantumSchedulingEnv") -> float:
    """
    非阻塞轮询已提交真机任务的结果，返回本步反馈 reward（Issue #64）。

    遍历 ``env._pending_real_tasks``，对每个任务调用 ``get_task_status`` 查询状态：
        - completed : 计入成功，返回 REAL_MACHINE_SUCCESS_BONUS
        - error     : 计入失败，返回 REAL_MACHINE_FAIL_PENALTY，触发降级判断
        - timeout   : 轮询次数超过 REAL_MACHINE_MAX_POLL_STEPS，视为超时失败
        - running/unknown : poll_count +1，保留在 pending 列表

    所有反馈乘以 ``env.real_machine_feedback_weight`` 后累加返回。

    Args:
        env: 调度环境实例

    Returns:
        本步真机反馈 reward（正为成功加成，负为失败惩罚，0 表示无新结果）
    """
    if not env._pending_real_tasks:
        return 0.0

    total_feedback = 0.0
    still_pending: list[dict[str, Any]] = []

    for pending in env._pending_real_tasks:
        pending["poll_count"] += 1
        machine_name = pending["machine_name"]
        real_task_id = pending["task_id"]
        task_id_str = pending["task_id_str"]
        client = env._real_clients.get(machine_name)

        # 客户端丢失（理论上不应发生），视为失败
        if client is None:
            total_feedback += REAL_MACHINE_FAIL_PENALTY * env.real_machine_feedback_weight
            record_real_failure(env, machine_name, "客户端丢失")
            continue

        try:
            status = client.get_task_status(real_task_id)
        except Exception as e:
            # 查询异常视为本步未拿到结果，保留在 pending 列表
            logger.debug(f"[真机闭环] 查询 {real_task_id} 异常: {e}")
            still_pending.append(pending)
            continue

        status_str = str(status.get("status", "unknown"))

        if status_str == "completed":
            # 真机成功：正向反馈
            total_feedback += (
                REAL_MACHINE_SUCCESS_BONUS * env.real_machine_feedback_weight
            )
            env._real_success_count += 1
            env._real_consecutive_failures = 0  # 成功重置连续失败计数
            logger.debug(
                f"[真机闭环] 任务 {task_id_str} 真机执行成功 "
                f"(machine={machine_name}, real_task_id={real_task_id})"
            )
        elif status_str == "error":
            # 真机失败：负向反馈 + 降级判断
            total_feedback += (
                REAL_MACHINE_FAIL_PENALTY * env.real_machine_feedback_weight
            )
            record_real_failure(env, machine_name, "任务状态=error")
        elif pending["poll_count"] >= REAL_MACHINE_MAX_POLL_STEPS:
            # 超时：视为失败
            total_feedback += (
                REAL_MACHINE_FAIL_PENALTY * env.real_machine_feedback_weight
            )
            record_real_failure(env, machine_name, "轮询超时")
            logger.debug(
                f"[真机闭环] 任务 {task_id_str} 轮询超时 "
                f"(poll_count={pending['poll_count']})"
            )
        else:
            # 仍在运行，保留到下一步轮询
            still_pending.append(pending)

    env._pending_real_tasks = still_pending
    return total_feedback
