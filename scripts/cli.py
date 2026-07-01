"""量子RL调度系统 — 统一 CLI 入口

将分散的训练/仿真/服务/演示脚本聚合为单一命令行入口，降低使用心智成本。

用法:
    python scripts/cli.py train --timesteps 100000 --algorithm ppo
    python scripts/cli.py simulate --num-tasks 200
    python scripts/cli.py serve --port 8000
    python scripts/cli.py demo --multi-machine
"""

import os
import sys

# 确保项目根目录在 sys.path 中，便于导入 src 与 scripts 模块
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import click


@click.group()
def cli() -> None:
    """量子RL调度系统 CLI — 统一入口（训练/仿真/服务/演示）。"""


@cli.command()
@click.option("--timesteps", default=50000, show_default=True, help="训练总步数")
@click.option(
    "--algorithm",
    type=click.Choice(["ppo", "dqn"]),
    default="ppo",
    show_default=True,
    help="RL 算法（PPO 为主力，DQN 为备选）",
)
@click.option("--max-qubits", default=20, show_default=True, help="最大量子比特数")
@click.option("--seed", default=42, show_default=True, help="随机种子")
@click.option(
    "--save-path",
    default="models/cli_model",
    show_default=True,
    help="模型保存路径（不含扩展名）",
)
def train(
    timesteps: int,
    algorithm: str,
    max_qubits: int,
    seed: int,
    save_path: str,
) -> None:
    """训练调度模型（PPO 主力 / DQN 备选）。"""
    click.echo(
        f"🚀 开始训练: algorithm={algorithm}, timesteps={timesteps}, "
        f"max_qubits={max_qubits}, seed={seed}"
    )
    try:
        from src.scheduler.agent import PPOAgent, SchedulerAgent
        from src.scheduler.env import QuantumSchedulingEnv
    except ImportError as exc:
        click.echo(f"[错误] 无法导入训练模块: {exc}", err=True)
        click.echo("  请确保从项目根目录运行，且已安装所有依赖。", err=True)
        sys.exit(1)

    env = QuantumSchedulingEnv(max_qubits=max_qubits)
    try:
        if algorithm == "ppo":
            agent = PPOAgent(
                env,
                learning_rate=3e-4,
                n_steps=2048,
                gamma=0.99,
                seed=seed,
            )
            agent.train(total_timesteps=timesteps, log_dir="./logs/cli_train")
        else:
            agent = SchedulerAgent(
                env,
                learning_rate=1e-4,
                batch_size=32,
                gamma=0.99,
                seed=seed,
            )
            agent.train(
                total_timesteps=timesteps,
                eval_freq=max(timesteps // 10, 1),
                log_dir="./logs/cli_train",
            )
        agent.save(save_path)
    except Exception as exc:  # CLI 顶层兜底，需向用户暴露失败原因
        click.echo(f"[错误] 训练失败: {exc}", err=True)
        sys.exit(1)
    click.echo(f"✅ 训练完成，模型已保存到: {save_path}")


@cli.command()
@click.option("--num-tasks", default=200, show_default=True, help="每个 episode 的模拟任务数")
@click.option("--episodes", default=20, show_default=True, help="仿真 episode 数")
@click.option(
    "--mock-mode", is_flag=True, default=True, help="使用 Mock 模式（纯仿真，不抽样真机）"
)
@click.option("--model-path", default=None, help="训练好的 DQN 模型路径（.zip 文件，可选）")
@click.option("--ppo-model-path", default=None, help="训练好的 PPO 模型路径（.zip 文件，可选）")
@click.option("--output-dir", default="./results/", show_default=True, help="结果输出目录")
@click.option("--verbose", is_flag=True, default=False, help="打印详细的逐 episode 日志")
def simulate(
    num_tasks: int,
    episodes: int,
    mock_mode: bool,
    model_path: str | None,
    ppo_model_path: str | None,
    output_dir: str,
    verbose: bool,
) -> None:
    """运行调度仿真对比（7-8 种策略）。"""
    click.echo(
        f"📊 开始仿真: episodes={episodes}, tasks/episode={num_tasks}, " f"mock_mode={mock_mode}"
    )
    try:
        from scripts.run_simulation import run_simulation
    except ImportError as exc:
        click.echo(f"[错误] 无法导入仿真脚本: {exc}", err=True)
        click.echo("  请确保从项目根目录运行，且已安装所有依赖。", err=True)
        sys.exit(1)

    # Mock 模式下不启用真机抽样，real_prob=0 表示纯仿真
    real_prob = 0.0
    try:
        run_simulation(
            episodes=episodes,
            tasks_per_episode=num_tasks,
            model_path=model_path,
            ppo_model_path=ppo_model_path,
            output_dir=output_dir,
            verbose=verbose,
            real_prob=real_prob,
        )
    except Exception as exc:  # CLI 顶层兜底，需向用户暴露失败原因
        click.echo(f"[错误] 仿真失败: {exc}", err=True)
        sys.exit(1)
    click.echo("✅ 仿真完成")


@cli.command()
@click.option("--port", default=8000, show_default=True, help="Web 服务端口")
@click.option("--host", default="0.0.0.0", show_default=True, help="绑定地址")
def serve(port: int, host: str) -> None:
    """启动 Web 监控面板（FastAPI + Uvicorn）。"""
    click.echo(f"🌐 启动 Web 服务: http://{host}:{port}")
    try:
        from src.visualization.app import start_web_server
    except ImportError as exc:
        click.echo(f"[错误] 无法导入可视化模块: {exc}", err=True)
        click.echo("  请确保已安装 fastapi、uvicorn 等依赖。", err=True)
        sys.exit(1)
    try:
        start_web_server(host=host, port=port)
    except Exception as exc:  # CLI 顶层兜底，需向用户暴露失败原因
        click.echo(f"[错误] Web 服务启动失败: {exc}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--multi-machine",
    is_flag=True,
    default=False,
    help="多机器调度演示（演示本身会对比单机 vs 多机器，此标志用于显式确认）",
)
@click.option("--real", is_flag=True, default=False, help="真机验证模式（需配置 TIANYAN_API_KEY）")
@click.option("--episodes", default=20, show_default=True, help="每个场景的演示轮数")
@click.option(
    "--ppo-model",
    default="models/ppo_seed_42_v4/best_model.zip",
    show_default=True,
    help="PPO 模型路径（不存在则使用启发式策略）",
)
@click.option(
    "--output",
    default="results/multi_machine_demo_report.md",
    show_default=True,
    help="报告输出路径",
)
def demo(
    multi_machine: bool,
    real: bool,
    episodes: int,
    ppo_model: str,
    output: str,
) -> None:
    """运行调度演示（单机 vs 多机器 / 真机验证）。"""
    click.echo(f"🎯 演示模式: multi_machine={multi_machine}, real={real}, episodes={episodes}")
    try:
        from scripts.demo_multi_machine import main as demo_main
    except ImportError as exc:
        click.echo(f"[错误] 无法导入演示脚本: {exc}", err=True)
        click.echo("  请确保从项目根目录运行，且已安装所有依赖。", err=True)
        sys.exit(1)

    # demo_multi_machine.main() 使用 argparse 解析命令行参数，
    # 通过临时覆写 sys.argv 复用其完整逻辑（含真机客户端构造、报告生成）。
    argv = [
        "demo_multi_machine.py",
        "--episodes",
        str(episodes),
        "--ppo-model",
        ppo_model,
        "--output",
        output,
    ]
    if real:
        argv.append("--real")
    sys.argv = argv
    try:
        demo_main()
    except SystemExit:
        # argparse 在遇到 --help 等情况会调用 sys.exit，捕获以避免 CLI 异常退出
        pass
    except Exception as exc:  # CLI 顶层兜底，需向用户暴露失败原因
        click.echo(f"[错误] 演示失败: {exc}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
