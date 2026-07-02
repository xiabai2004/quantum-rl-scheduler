"""
天衍云 cqlib SDK 封装
Cqlib Wrapper for Tianyan Cloud Platform

基于官方 cqlib 库封装的量子任务客户端，支持：
- 真机任务提交（QCIS 格式）
- 任务状态查询与结果获取
- 量子计算机列表查询
- 自动重试和异常处理

使用前需安装：pip install cqlib
"""

import time
from typing import Any

from loguru import logger


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁCqlibTianyanClientǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁauthenticate__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁget_backend_info__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁget_task_result__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut: MutantDict = {}  # type: ignore


class CqlibTianyanClient:
    """基于 cqlib SDK 的天衍云真机客户端

    直接调用天衍云超导量子计算机执行量子电路。

    使用示例::

        client = CqlibTianyanClient(login_key="your_key")
        task_id = client.submit_quantum_task(qcis="H Q0\\nM Q0", shots=1024)
        result = client.wait_for_task(task_id)
    """

    # 已知可用的超导真机
    REAL_MACHINES = [  # noqa: RUF012
        "tianyan_sw",  # 超导 free
        "tianyan_s",  # 超导 free
        "tianyan_tn",  # 超导 free
        "tianyan_tnn",  # 超导 free
        "tianyan_swn",  # 超导 free
        "tianyan_sa",  # 超导 free
        "tianyan176",  # 176比特 free
        "tianyan176-2",  # 176比特 free
    ]

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁ__init____mutmut)
    def __init__(
        self,
        login_key: str,
        machine_name: str = "tianyan_s",
        auto_retry_machine: bool = True,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = cqlib
        self.login_key = login_key
        self.machine_name = machine_name
        self.auto_retry_machine = auto_retry_machine
        self._platform = None

        logger.info(f"[Cqlib] 客户端初始化，默认机器={machine_name}")

    def xǁCqlibTianyanClientǁ__init____mutmut_orig(
        self,
        login_key: str,
        machine_name: str = "tianyan_s",
        auto_retry_machine: bool = True,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = cqlib
        self.login_key = login_key
        self.machine_name = machine_name
        self.auto_retry_machine = auto_retry_machine
        self._platform = None

        logger.info(f"[Cqlib] 客户端初始化，默认机器={machine_name}")

    def xǁCqlibTianyanClientǁ__init____mutmut_1(
        self,
        login_key: str,
        machine_name: str = "XXtianyan_sXX",
        auto_retry_machine: bool = True,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = cqlib
        self.login_key = login_key
        self.machine_name = machine_name
        self.auto_retry_machine = auto_retry_machine
        self._platform = None

        logger.info(f"[Cqlib] 客户端初始化，默认机器={machine_name}")

    def xǁCqlibTianyanClientǁ__init____mutmut_2(
        self,
        login_key: str,
        machine_name: str = "TIANYAN_S",
        auto_retry_machine: bool = True,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = cqlib
        self.login_key = login_key
        self.machine_name = machine_name
        self.auto_retry_machine = auto_retry_machine
        self._platform = None

        logger.info(f"[Cqlib] 客户端初始化，默认机器={machine_name}")

    def xǁCqlibTianyanClientǁ__init____mutmut_3(
        self,
        login_key: str,
        machine_name: str = "tianyan_s",
        auto_retry_machine: bool = False,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = cqlib
        self.login_key = login_key
        self.machine_name = machine_name
        self.auto_retry_machine = auto_retry_machine
        self._platform = None

        logger.info(f"[Cqlib] 客户端初始化，默认机器={machine_name}")

    def xǁCqlibTianyanClientǁ__init____mutmut_4(
        self,
        login_key: str,
        machine_name: str = "tianyan_s",
        auto_retry_machine: bool = True,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = None
        self.login_key = login_key
        self.machine_name = machine_name
        self.auto_retry_machine = auto_retry_machine
        self._platform = None

        logger.info(f"[Cqlib] 客户端初始化，默认机器={machine_name}")

    def xǁCqlibTianyanClientǁ__init____mutmut_5(
        self,
        login_key: str,
        machine_name: str = "tianyan_s",
        auto_retry_machine: bool = True,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = cqlib
        self.login_key = None
        self.machine_name = machine_name
        self.auto_retry_machine = auto_retry_machine
        self._platform = None

        logger.info(f"[Cqlib] 客户端初始化，默认机器={machine_name}")

    def xǁCqlibTianyanClientǁ__init____mutmut_6(
        self,
        login_key: str,
        machine_name: str = "tianyan_s",
        auto_retry_machine: bool = True,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = cqlib
        self.login_key = login_key
        self.machine_name = None
        self.auto_retry_machine = auto_retry_machine
        self._platform = None

        logger.info(f"[Cqlib] 客户端初始化，默认机器={machine_name}")

    def xǁCqlibTianyanClientǁ__init____mutmut_7(
        self,
        login_key: str,
        machine_name: str = "tianyan_s",
        auto_retry_machine: bool = True,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = cqlib
        self.login_key = login_key
        self.machine_name = machine_name
        self.auto_retry_machine = None
        self._platform = None

        logger.info(f"[Cqlib] 客户端初始化，默认机器={machine_name}")

    def xǁCqlibTianyanClientǁ__init____mutmut_8(
        self,
        login_key: str,
        machine_name: str = "tianyan_s",
        auto_retry_machine: bool = True,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = cqlib
        self.login_key = login_key
        self.machine_name = machine_name
        self.auto_retry_machine = auto_retry_machine
        self._platform = ""

        logger.info(f"[Cqlib] 客户端初始化，默认机器={machine_name}")

    def xǁCqlibTianyanClientǁ__init____mutmut_9(
        self,
        login_key: str,
        machine_name: str = "tianyan_s",
        auto_retry_machine: bool = True,
    ):
        """初始化 cqlib 客户端

        Args:
            login_key: API Key（从个人中心获取）
            machine_name: 默认使用的量子计算机名称
            auto_retry_machine: 当前机器不可用时是否自动切换
        """
        import cqlib

        self.cqlib = cqlib
        self.login_key = login_key
        self.machine_name = machine_name
        self.auto_retry_machine = auto_retry_machine
        self._platform = None

        logger.info(None)

    @property
    def platform(self) -> Any:
        """懒加载平台连接"""
        if self._platform is None:
            self._platform = self.cqlib.TianYanPlatform(
                login_key=self.login_key,
                machine_name=self.machine_name,
            )
        return self._platform

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁauthenticate__mutmut)
    def authenticate(self) -> bool:
        """验证 API Key 有效性"""
        try:
            _ = self.platform
            return True
        except Exception as e:
            logger.error(f"[Cqlib] 认证失败: {e}")
            return False

    def xǁCqlibTianyanClientǁauthenticate__mutmut_orig(self) -> bool:
        """验证 API Key 有效性"""
        try:
            _ = self.platform
            return True
        except Exception as e:
            logger.error(f"[Cqlib] 认证失败: {e}")
            return False

    def xǁCqlibTianyanClientǁauthenticate__mutmut_1(self) -> bool:
        """验证 API Key 有效性"""
        try:
            _ = None
            return True
        except Exception as e:
            logger.error(f"[Cqlib] 认证失败: {e}")
            return False

    def xǁCqlibTianyanClientǁauthenticate__mutmut_2(self) -> bool:
        """验证 API Key 有效性"""
        try:
            _ = self.platform
            return False
        except Exception as e:
            logger.error(f"[Cqlib] 认证失败: {e}")
            return False

    def xǁCqlibTianyanClientǁauthenticate__mutmut_3(self) -> bool:
        """验证 API Key 有效性"""
        try:
            _ = self.platform
            return True
        except Exception as e:
            logger.error(None)
            return False

    def xǁCqlibTianyanClientǁauthenticate__mutmut_4(self) -> bool:
        """验证 API Key 有效性"""
        try:
            _ = self.platform
            return True
        except Exception as e:
            logger.error(f"[Cqlib] 认证失败: {e}")
            return True

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁlist_backends__mutmut)
    def list_backends(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "type": m[1],
                    "status": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_orig(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "type": m[1],
                    "status": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_1(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = None
            return [
                {
                    "id": m[0],
                    "type": m[1],
                    "status": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_2(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "XXidXX": m[0],
                    "type": m[1],
                    "status": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_3(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "ID": m[0],
                    "type": m[1],
                    "status": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_4(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[1],
                    "type": m[1],
                    "status": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_5(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "XXtypeXX": m[1],
                    "status": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_6(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "TYPE": m[1],
                    "status": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_7(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "type": m[2],
                    "status": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_8(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "type": m[1],
                    "XXstatusXX": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_9(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "type": m[1],
                    "STATUS": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_10(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "type": m[1],
                    "status": m[3],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_11(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "type": m[1],
                    "status": m[2],
                    "XXnameXX": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_12(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "type": m[1],
                    "status": m[2],
                    "NAME": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_13(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "type": m[1],
                    "status": m[2],
                    "name": m[4],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(f"[Cqlib] 获取机器列表失败: {e}")
            return []

    def xǁCqlibTianyanClientǁlist_backends__mutmut_14(self) -> list[dict[str, Any]]:
        """列出所有可用的量子计算机"""
        try:
            machines = self.platform.query_quantum_computer_list()
            return [
                {
                    "id": m[0],
                    "type": m[1],
                    "status": m[2],
                    "name": m[3],
                }
                for m in machines
            ]
        except Exception as e:
            logger.error(None)
            return []

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁget_backend_info__mutmut)
    def get_backend_info(self, backend_name: str | None = None) -> dict[str, Any]:
        """获取指定后端信息"""
        name = backend_name or self.machine_name
        machines = self.list_backends()
        for m in machines:
            if m["name"] == name:
                return m
        return {}

    def xǁCqlibTianyanClientǁget_backend_info__mutmut_orig(self, backend_name: str | None = None) -> dict[str, Any]:
        """获取指定后端信息"""
        name = backend_name or self.machine_name
        machines = self.list_backends()
        for m in machines:
            if m["name"] == name:
                return m
        return {}

    def xǁCqlibTianyanClientǁget_backend_info__mutmut_1(self, backend_name: str | None = None) -> dict[str, Any]:
        """获取指定后端信息"""
        name = None
        machines = self.list_backends()
        for m in machines:
            if m["name"] == name:
                return m
        return {}

    def xǁCqlibTianyanClientǁget_backend_info__mutmut_2(self, backend_name: str | None = None) -> dict[str, Any]:
        """获取指定后端信息"""
        name = backend_name and self.machine_name
        machines = self.list_backends()
        for m in machines:
            if m["name"] == name:
                return m
        return {}

    def xǁCqlibTianyanClientǁget_backend_info__mutmut_3(self, backend_name: str | None = None) -> dict[str, Any]:
        """获取指定后端信息"""
        name = backend_name or self.machine_name
        machines = None
        for m in machines:
            if m["name"] == name:
                return m
        return {}

    def xǁCqlibTianyanClientǁget_backend_info__mutmut_4(self, backend_name: str | None = None) -> dict[str, Any]:
        """获取指定后端信息"""
        name = backend_name or self.machine_name
        machines = self.list_backends()
        for m in machines:
            if m["XXnameXX"] == name:
                return m
        return {}

    def xǁCqlibTianyanClientǁget_backend_info__mutmut_5(self, backend_name: str | None = None) -> dict[str, Any]:
        """获取指定后端信息"""
        name = backend_name or self.machine_name
        machines = self.list_backends()
        for m in machines:
            if m["NAME"] == name:
                return m
        return {}

    def xǁCqlibTianyanClientǁget_backend_info__mutmut_6(self, backend_name: str | None = None) -> dict[str, Any]:
        """获取指定后端信息"""
        name = backend_name or self.machine_name
        machines = self.list_backends()
        for m in machines:
            if m["name"] != name:
                return m
        return {}

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut)
    def submit_quantum_task(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_orig(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_1(
        self,
        qcis: str = "XXXX",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_2(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1025,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_3(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "XXScheduler_TaskXX",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_4(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "scheduler_task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_5(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "SCHEDULER_TASK",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_6(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = None
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_7(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_8(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = None
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_9(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(None, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_10(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, None) else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_11(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr("qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_12(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, ) else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_13(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "XXqcisXX") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_14(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "QCIS") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_15(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(None)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_16(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError(None)

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_17(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("XX必须提供 qcis 或 circuitXX")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_18(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 QCIS 或 CIRCUIT")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_19(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(None)
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_20(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(None)

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_21(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:101]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_22(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_23(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(None):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_24(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(None)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_25(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(None, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_26(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, None, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_27(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, None)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_28(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_29(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_30(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, )
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_31(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = None
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_32(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=None,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_33(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=None,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_34(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=None,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_35(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=None,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_36(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_37(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_38(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_39(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_40(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=True,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_41(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) or len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_42(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) >= 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_43(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 1:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_44(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = None
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_45(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(None)
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_46(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[1])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_47(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(None)
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_48(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(None)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_49(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = None
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_50(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(None)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_51(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(None)
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_52(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) or self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_53(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(None) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_54(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(None, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_55(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, None, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_56(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, None)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_57(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_58(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_59(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, )
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_60(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(None, shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_61(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, None, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_62(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, None)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_63(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(shots, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_64(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, task_name)
            return None

    def xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_65(
        self,
        qcis: str = "",
        circuit: Any = None,
        shots: int = 1024,
        task_name: str = "Scheduler_Task",
    ) -> str | None:
        """提交量子任务到真机（含故障自动切换）

        提交策略：
            1. 预检当前机器状态：若非 running（校准中/维护中），立即跳过，不重试
            2. 尝试在当前机器提交；失败时按 auto_retry_machine 切换备用机
            3. 所有机器不可用时返回 None（不抛异常，保证调度循环不中断）

        Args:
            qcis: QCIS 指令字符串（"H Q0\\nM Q0"）
            circuit: cqlib.Circuit 对象（与 qcis 二选一）
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部机器不可用时返回 None
        """
        # 生成 QCIS
        if qcis:
            qcis_str = qcis
        elif circuit is not None:
            qcis_str = circuit.qcis if hasattr(circuit, "qcis") else str(circuit)
        else:
            raise ValueError("必须提供 qcis 或 circuit")

        logger.info(f"[Cqlib] 提交量子任务: {task_name}, shots={shots}")
        logger.debug(f"[Cqlib] QCIS: {qcis_str[:100]}")

        # 预检当前机器状态（校准中/维护中立即跳过，不重试）
        if not self._is_machine_available(self.machine_name):
            logger.warning(f"[Cqlib] {self.machine_name} 不可用（校准/维护中），切换备用机")
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            return None

        try:
            result = self.platform.submit_experiment(
                circuit=qcis_str,
                name=task_name,
                num_shots=shots,
                is_verify=False,
            )
            if isinstance(result, list) and len(result) > 0:
                task_id = str(result[0])
                logger.info(f"[Cqlib] 任务已提交: {task_id}")
                return task_id
            return str(result)
        except Exception as e:
            err_msg = str(e)
            logger.error(f"[Cqlib] {self.machine_name} 提交失败: {err_msg}")
            # 校准/不可用类错误立即切换，不重试当前机器
            if self._is_unavailable_error(err_msg) and self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, task_name)
            if self.auto_retry_machine:
                return self._retry_other_machine(qcis_str, shots, )
            return None

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut)
    def _is_machine_available(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get("status") == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_orig(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get("status") == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_1(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = None
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get("status") == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_2(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get(None) == machine_name:
                    return m.get("status") == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_3(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("XXnameXX") == machine_name:
                    return m.get("status") == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_4(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("NAME") == machine_name:
                    return m.get("status") == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_5(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") != machine_name:
                    return m.get("status") == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_6(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get(None) == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_7(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get("XXstatusXX") == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_8(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get("STATUS") == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_9(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get("status") != "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_10(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get("status") == "XXrunningXX"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_11(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get("status") == "RUNNING"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_12(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get("status") == "running"
            # 未找到该机器，乐观放行
            return False
        except Exception:
            # 查询失败不阻塞，乐观放行
            return True

    def xǁCqlibTianyanClientǁ_is_machine_available__mutmut_13(self, machine_name: str) -> bool:
        """检查机器是否在线可用（status == running）。

        通过 query_quantum_computer_list 查询状态。查询本身失败时
        乐观返回 True（不阻塞提交，让 submit 自行暴露真实错误）。

        Args:
            machine_name: 机器名

        Returns:
            bool: running 返回 True，calibration/maintenance/unknown 返回 False
        """
        try:
            machines = self.list_backends()
            for m in machines:
                if m.get("name") == machine_name:
                    return m.get("status") == "running"
            # 未找到该机器，乐观放行
            return True
        except Exception:
            # 查询失败不阻塞，乐观放行
            return False

    @staticmethod
    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut)
    def _is_unavailable_error(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_orig(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_1(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = None
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_2(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "XX校准XX",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_3(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "XXcalibrationXX",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_4(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "CALIBRATION",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_5(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "XX维护XX",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_6(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "XXmaintenanceXX",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_7(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "MAINTENANCE",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_8(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "XX不可用XX",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_9(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "XXunavailableXX",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_10(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "UNAVAILABLE",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_11(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "XX忙碌XX",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_12(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "XXbusyXX",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_13(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "BUSY",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_14(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "XXofflineXX",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_15(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "OFFLINE",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_16(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = None
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_17(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.upper()
        return any(kw.lower() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_18(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(None)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_19(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.upper() in lower_msg for kw in keywords)

    @staticmethod
    def xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_20(err_msg: str) -> bool:
        """判断错误是否为机器不可用（校准/维护/忙）类错误。

        Args:
            err_msg: 异常消息字符串

        Returns:
            bool: 命中关键词返回 True
        """
        keywords = (
            "校准",
            "calibration",
            "维护",
            "maintenance",
            "不可用",
            "unavailable",
            "忙碌",
            "busy",
            "offline",
        )
        lower_msg = err_msg.lower()
        return any(kw.lower() not in lower_msg for kw in keywords)

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut)
    def _retry_other_machine(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_orig(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_1(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine != self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_2(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                break
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_3(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_4(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(None):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_5(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(None)
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_6(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                break
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_7(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(None)
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_8(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = None
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_9(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=None,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_10(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=None,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_11(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_12(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_13(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = None
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_14(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=None,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_15(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=None,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_16(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=None,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_17(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=None,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_18(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_19(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_20(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_21(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_22(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=True,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_23(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) or len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_24(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) >= 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_25(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 1:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_26(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = None
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_27(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(None)
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_28(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[1])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_29(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(None)
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_30(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(None)
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_31(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(None)[:60]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_32(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:61]}")
                continue
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_33(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                break
        logger.error("[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_34(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error(None)
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_35(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("XX[Cqlib] 所有备用机器均不可用，放弃提交（返回 None）XX")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_36(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[cqlib] 所有备用机器均不可用，放弃提交（返回 none）")
        return None

    def xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_37(self, qcis: str, shots: int, task_name: str) -> str | None:
        """当前机器不可用时，按 REAL_MACHINES 列表尝试其他机器。

        每台候选机器先做可用性预检（跳过校准/维护中的），再尝试提交。
        全部不可用时返回 None（不抛异常）。

        Args:
            qcis: QCIS 指令字符串
            shots: 测量次数
            task_name: 任务名称

        Returns:
            task_id 字符串；全部失败返回 None
        """
        for machine in self.REAL_MACHINES:
            if machine == self.machine_name:
                continue
            # 预检：跳过不可用机器，避免无效重试
            if not self._is_machine_available(machine):
                logger.debug(f"[Cqlib] 跳过 {machine}（不可用）")
                continue
            try:
                logger.info(f"[Cqlib] 尝试备用机器: {machine}")
                alt = self.cqlib.TianYanPlatform(
                    login_key=self.login_key,
                    machine_name=machine,
                )
                result = alt.submit_experiment(
                    circuit=qcis,
                    name=task_name,
                    num_shots=shots,
                    is_verify=False,
                )
                if isinstance(result, list) and len(result) > 0:
                    tid = str(result[0])
                    logger.info(f"[Cqlib] {machine} 提交成功: {tid}")
                    return tid
            except Exception as e:
                logger.debug(f"[Cqlib] {machine} 失败: {str(e)[:60]}")
                continue
        logger.error("[CQLIB] 所有备用机器均不可用，放弃提交（返回 NONE）")
        return None

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁget_task_status__mutmut)
    def get_task_status(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_orig(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_1(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = None
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_2(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(None)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_3(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) or len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_4(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) >= 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_5(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 1:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_6(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = None
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_7(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[1]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_8(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = None
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_9(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data and "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_10(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "XXresultStatusXX" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_11(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultstatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_12(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "RESULTSTATUS" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_13(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" not in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_14(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "XXprobabilityXX" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_15(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "PROBABILITY" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_16(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" not in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_17(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "XXtask_idXX": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_18(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "TASK_ID": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_19(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "XXstatusXX": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_20(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "STATUS": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_21(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "XXcompletedXX" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_22(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "COMPLETED" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_23(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "XXrunningXX",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_24(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "RUNNING",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_25(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "XXresultXX": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_26(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "RESULT": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_27(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get(None),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_28(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("XXprobabilityXX"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_29(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("PROBABILITY"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_30(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "XXrawXX": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_31(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "RAW": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_32(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"XXtask_idXX": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_33(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"TASK_ID": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_34(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "XXstatusXX": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_35(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "STATUS": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_36(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "XXunknownXX", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_37(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "UNKNOWN", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_38(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "XXrawXX": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_39(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "RAW": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_40(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"XXtask_idXX": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_41(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"TASK_ID": task_id, "status": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_42(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "XXstatusXX": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_43(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "STATUS": "error", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_44(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "XXerrorXX", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_45(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "ERROR", "error": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_46(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "XXerrorXX": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_47(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "ERROR": str(e)}

    def xǁCqlibTianyanClientǁget_task_status__mutmut_48(self, task_id: str) -> dict[str, Any]:
        """查询任务状态"""
        try:
            result = self.platform.query_experiment(task_id)
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                if isinstance(data, dict):
                    has_result = "resultStatus" in data or "probability" in data
                    return {
                        "task_id": task_id,
                        "status": "completed" if has_result else "running",
                        "result": data.get("probability"),
                        "raw": data,
                    }
            return {"task_id": task_id, "status": "unknown", "raw": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(None)}

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁget_task_result__mutmut)
    def get_task_result(self, task_id: str) -> dict[str, Any]:
        """获取任务执行结果"""
        return self.get_task_status(task_id)

    def xǁCqlibTianyanClientǁget_task_result__mutmut_orig(self, task_id: str) -> dict[str, Any]:
        """获取任务执行结果"""
        return self.get_task_status(task_id)

    def xǁCqlibTianyanClientǁget_task_result__mutmut_1(self, task_id: str) -> dict[str, Any]:
        """获取任务执行结果"""
        return self.get_task_status(None)

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut)
    def wait_for_task(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_orig(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_1(
        self, task_id: str, timeout: int = 301, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_2(
        self, task_id: str, timeout: int = 300, poll_interval: int = 6
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_3(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = None
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_4(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() + start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_5(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start <= timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_6(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = None
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_7(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(None)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_8(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["XXstatusXX"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_9(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["STATUS"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_10(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] != "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_11(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "XXcompletedXX":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_12(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "COMPLETED":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_13(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["XXstatusXX"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_14(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["STATUS"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_15(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] != "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_16(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "XXerrorXX":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_17(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "ERROR":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_18(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(None)
        return {"task_id": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_19(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"XXtask_idXX": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_20(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"TASK_ID": task_id, "status": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_21(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "XXstatusXX": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_22(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "STATUS": "timeout"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_23(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "XXtimeoutXX"}

    def xǁCqlibTianyanClientǁwait_for_task__mutmut_24(
        self, task_id: str, timeout: int = 300, poll_interval: int = 5
    ) -> dict[str, Any]:
        """轮询等待任务完成并返回结果

        Args:
            task_id: 任务 ID
            timeout: 超时秒数
            poll_interval: 轮询间隔秒数
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(task_id)
            if status["status"] == "completed":
                return status
            if status["status"] == "error":
                return status
            time.sleep(poll_interval)
        return {"task_id": task_id, "status": "TIMEOUT"}

    @_mutmut_mutated(mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut)
    def get_queue_status(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_orig(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_1(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = None
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_2(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = None
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_3(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(None)
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_4(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(2 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_5(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get(None) == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_6(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("XXstatusXX") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_7(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("STATUS") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_8(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") != "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_9(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "XXrunningXX")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_10(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "RUNNING")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_11(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "XXtotal_machinesXX": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_12(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "TOTAL_MACHINES": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_13(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "XXrunningXX": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_14(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "RUNNING": running,
            "available": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_15(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "XXavailableXX": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_16(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "AVAILABLE": [m["name"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_17(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["XXnameXX"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_18(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["NAME"] for m in machines if m["status"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_19(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["XXstatusXX"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_20(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["STATUS"] == "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_21(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] != "running"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_22(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "XXrunningXX"],
        }

    def xǁCqlibTianyanClientǁget_queue_status__mutmut_23(self) -> dict[str, Any]:
        """获取队列状态（cqlib 无此接口，返回估算）"""
        machines = self.list_backends()
        running = sum(1 for m in machines if m.get("status") == "running")
        return {
            "total_machines": len(machines),
            "running": running,
            "available": [m["name"] for m in machines if m["status"] == "RUNNING"],
        }

mutants_xǁCqlibTianyanClientǁ__init____mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ__init____mutmut['xǁCqlibTianyanClientǁ__init____mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ__init____mutmut['xǁCqlibTianyanClientǁ__init____mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ__init____mutmut['xǁCqlibTianyanClientǁ__init____mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ__init____mutmut['xǁCqlibTianyanClientǁ__init____mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ__init____mutmut['xǁCqlibTianyanClientǁ__init____mutmut_5'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ__init____mutmut['xǁCqlibTianyanClientǁ__init____mutmut_6'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ__init____mutmut['xǁCqlibTianyanClientǁ__init____mutmut_7'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ__init____mutmut['xǁCqlibTianyanClientǁ__init____mutmut_8'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ__init____mutmut['xǁCqlibTianyanClientǁ__init____mutmut_9'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ__init____mutmut_9 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁauthenticate__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁauthenticate__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁauthenticate__mutmut['xǁCqlibTianyanClientǁauthenticate__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁauthenticate__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁauthenticate__mutmut['xǁCqlibTianyanClientǁauthenticate__mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁauthenticate__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁauthenticate__mutmut['xǁCqlibTianyanClientǁauthenticate__mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁauthenticate__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁauthenticate__mutmut['xǁCqlibTianyanClientǁauthenticate__mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁauthenticate__mutmut_4 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_5'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_6'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_7'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_8'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_9'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_10'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_11'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_12'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_13'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁlist_backends__mutmut['xǁCqlibTianyanClientǁlist_backends__mutmut_14'] = CqlibTianyanClient.xǁCqlibTianyanClientǁlist_backends__mutmut_14 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁget_backend_info__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_backend_info__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_backend_info__mutmut['xǁCqlibTianyanClientǁget_backend_info__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_backend_info__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_backend_info__mutmut['xǁCqlibTianyanClientǁget_backend_info__mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_backend_info__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_backend_info__mutmut['xǁCqlibTianyanClientǁget_backend_info__mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_backend_info__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_backend_info__mutmut['xǁCqlibTianyanClientǁget_backend_info__mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_backend_info__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_backend_info__mutmut['xǁCqlibTianyanClientǁget_backend_info__mutmut_5'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_backend_info__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_backend_info__mutmut['xǁCqlibTianyanClientǁget_backend_info__mutmut_6'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_backend_info__mutmut_6 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_5'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_6'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_7'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_8'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_9'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_10'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_11'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_12'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_13'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_14'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_15'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_16'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_17'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_18'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_19'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_20'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_21'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_22'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_23'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_24'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_25'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_26'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_27'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_28'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_29'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_30'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_31'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_32'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_33'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_34'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_35'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_36'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_37'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_38'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_38 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_39'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_39 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_40'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_40 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_41'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_41 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_42'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_42 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_43'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_43 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_44'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_44 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_45'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_45 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_46'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_46 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_47'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_47 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_48'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_48 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_49'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_49 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_50'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_50 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_51'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_51 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_52'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_52 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_53'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_53 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_54'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_54 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_55'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_55 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_56'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_56 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_57'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_57 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_58'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_58 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_59'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_59 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_60'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_60 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_61'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_61 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_62'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_62 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_63'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_63 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_64'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_64 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut['xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_65'] = CqlibTianyanClient.xǁCqlibTianyanClientǁsubmit_quantum_task__mutmut_65 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_5'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_6'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_7'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_8'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_9'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_10'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_11'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_12'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_machine_available__mutmut['xǁCqlibTianyanClientǁ_is_machine_available__mutmut_13'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_machine_available__mutmut_13 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_5'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_6'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_7'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_8'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_9'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_10'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_11'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_12'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_13'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_14'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_15'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_16'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_17'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_18'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_19'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut['xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_20'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_is_unavailable_error__mutmut_20 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_5'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_6'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_7'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_8'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_9'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_10'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_11'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_12'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_13'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_14'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_15'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_16'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_17'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_18'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_19'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_20'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_21'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_22'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_23'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_24'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_25'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_26'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_27'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_28'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_29'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_30'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_31'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_32'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_33'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_34'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_35'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_36'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁ_retry_other_machine__mutmut['xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_37'] = CqlibTianyanClient.xǁCqlibTianyanClientǁ_retry_other_machine__mutmut_37 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_5'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_6'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_7'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_8'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_9'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_10'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_11'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_12'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_13'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_14'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_15'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_16'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_17'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_18'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_19'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_20'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_21'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_22'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_23'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_24'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_25'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_26'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_27'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_28'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_29'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_30'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_31'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_32'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_33'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_34'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_35'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_36'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_37'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_38'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_38 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_39'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_39 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_40'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_40 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_41'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_41 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_42'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_42 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_43'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_43 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_44'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_44 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_45'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_45 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_46'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_46 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_47'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_47 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_status__mutmut['xǁCqlibTianyanClientǁget_task_status__mutmut_48'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_status__mutmut_48 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁget_task_result__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_result__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_task_result__mutmut['xǁCqlibTianyanClientǁget_task_result__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_task_result__mutmut_1 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_5'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_6'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_7'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_8'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_9'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_10'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_11'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_12'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_13'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_14'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_15'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_16'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_17'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_18'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_19'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_20'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_21'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_22'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_23'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁwait_for_task__mutmut['xǁCqlibTianyanClientǁwait_for_task__mutmut_24'] = CqlibTianyanClient.xǁCqlibTianyanClientǁwait_for_task__mutmut_24 # type: ignore # mutmut generated

mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['_mutmut_orig'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_1'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_2'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_3'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_4'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_5'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_6'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_7'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_8'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_9'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_10'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_11'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_12'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_13'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_14'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_15'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_16'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_17'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_18'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_19'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_20'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_21'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_22'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCqlibTianyanClientǁget_queue_status__mutmut['xǁCqlibTianyanClientǁget_queue_status__mutmut_23'] = CqlibTianyanClient.xǁCqlibTianyanClientǁget_queue_status__mutmut_23 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut: MutantDict = {}  # type: ignore


class MultiMachineCqlibCoordinator:
    """多机器 cqlib 协调器：统一管理多台天衍云真机的提交与状态聚合。

    每台机器对应一个独立的 CqlibTianyanClient 实例（独立 platform 连接），
    本协调器负责按机器名分发任务、聚合队列状态、汇总真机提交计数。

    使用示例::

        coord = MultiMachineCqlibCoordinator(
            login_key="xxx",
            machine_names=["tianyan_s", "tianyan_sw", "tianyan_tn"],
        )
        task_id = coord.submit_to_machine("tianyan_s", "H Q0\\nM Q0", shots=512)
        status = coord.get_all_status()
    """

    @_mutmut_mutated(mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut)
    def __init__(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_orig(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_1(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = True,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_2(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = None
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_3(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = None
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_4(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(None)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_5(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = None
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_6(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = None
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_7(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = None
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_8(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(None, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_9(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, None)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_10(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_11(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, )
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_12(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 1)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_13(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = None

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_14(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(None, 0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_15(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, None)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_16(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(0)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_17(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, )

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_18(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 1)

        logger.info(f"[MultiMachine] 纳管 {len(self.machine_names)} 台机器: {self.machine_names}")

    def xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_19(
        self,
        login_key: str,
        machine_names: list[str],
        auto_retry_machine: bool = False,
    ):
        """初始化多机器协调器。

        Args:
            login_key        : 天衍云 API Key
            machine_names    : 要纳管的机器名列表
            auto_retry_machine: 单机提交失败时是否自动切换其他机器（默认 False，
                               多机器场景下由调度器决定路由，通常关闭单机重试）
        """
        self.login_key = login_key
        self.machine_names = list(machine_names)
        self.auto_retry_machine = auto_retry_machine
        self._clients: dict[str, CqlibTianyanClient] = {}
        self._submit_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)
        self._fail_count: dict[str, int] = dict.fromkeys(self.machine_names, 0)

        logger.info(None)

    @_mutmut_mutated(mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut)
    def _get_client(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = CqlibTianyanClient(
                login_key=self.login_key,
                machine_name=machine_name,
                auto_retry_machine=self.auto_retry_machine,
            )
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_orig(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = CqlibTianyanClient(
                login_key=self.login_key,
                machine_name=machine_name,
                auto_retry_machine=self.auto_retry_machine,
            )
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_1(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = CqlibTianyanClient(
                login_key=self.login_key,
                machine_name=machine_name,
                auto_retry_machine=self.auto_retry_machine,
            )
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_2(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = CqlibTianyanClient(
                login_key=self.login_key,
                machine_name=machine_name,
                auto_retry_machine=self.auto_retry_machine,
            )
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_3(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(None)
            self._clients[machine_name] = CqlibTianyanClient(
                login_key=self.login_key,
                machine_name=machine_name,
                auto_retry_machine=self.auto_retry_machine,
            )
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_4(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = None
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_5(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = CqlibTianyanClient(
                login_key=None,
                machine_name=machine_name,
                auto_retry_machine=self.auto_retry_machine,
            )
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_6(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = CqlibTianyanClient(
                login_key=self.login_key,
                machine_name=None,
                auto_retry_machine=self.auto_retry_machine,
            )
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_7(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = CqlibTianyanClient(
                login_key=self.login_key,
                machine_name=machine_name,
                auto_retry_machine=None,
            )
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_8(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = CqlibTianyanClient(
                machine_name=machine_name,
                auto_retry_machine=self.auto_retry_machine,
            )
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_9(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = CqlibTianyanClient(
                login_key=self.login_key,
                auto_retry_machine=self.auto_retry_machine,
            )
        return self._clients[machine_name]

    def xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_10(self, machine_name: str) -> CqlibTianyanClient:
        """懒加载指定机器的客户端（避免初始化时连接所有机器）。"""
        if machine_name not in self._clients:
            if machine_name not in self.machine_names:
                raise ValueError(f"机器 {machine_name} 未被纳管")
            self._clients[machine_name] = CqlibTianyanClient(
                login_key=self.login_key,
                machine_name=machine_name,
                )
        return self._clients[machine_name]

    @_mutmut_mutated(mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut)
    def submit_to_machine(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_orig(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_1(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 513,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_2(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "XXMultiMachine_TaskXX",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_3(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "multimachine_task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_4(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MULTIMACHINE_TASK",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_5(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = None
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_6(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(None)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_7(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = None
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_8(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=None, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_9(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=None, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_10(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=None)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_11(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_12(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_13(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, )
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_14(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = None
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_15(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) - 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_16(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(None, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_17(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, None) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_18(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_19(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, ) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_20(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 1) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_21(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 2
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_22(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = None
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_23(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) - 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_24(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(None, 0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_25(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, None) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_26(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(0) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_27(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, ) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_28(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 1) + 1
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_29(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 2
            logger.error(f"[MultiMachine] {machine_name} 提交失败: {e}")
            return None

    def xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_30(
        self,
        machine_name: str,
        qcis: str,
        shots: int = 512,
        task_name: str = "MultiMachine_Task",
    ) -> str | None:
        """向指定机器提交量子任务。

        Args:
            machine_name: 目标机器名
            qcis        : QCIS 指令字符串
            shots       : 测量次数
            task_name   : 任务名称

        Returns:
            task_id 字符串；提交失败返回 None
        """
        try:
            client = self._get_client(machine_name)
            task_id = client.submit_quantum_task(qcis=qcis, shots=shots, task_name=task_name)
            self._submit_count[machine_name] = self._submit_count.get(machine_name, 0) + 1
            return task_id
        except Exception as e:
            self._fail_count[machine_name] = self._fail_count.get(machine_name, 0) + 1
            logger.error(None)
            return None

    @_mutmut_mutated(mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut)
    def get_all_status(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = {}
        for name in self.machine_names:
            try:
                client = self._get_client(name)
                status[name] = client.get_queue_status()
            except Exception as e:
                status[name] = {"error": str(e)[:80]}
        return status

    def xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_orig(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = {}
        for name in self.machine_names:
            try:
                client = self._get_client(name)
                status[name] = client.get_queue_status()
            except Exception as e:
                status[name] = {"error": str(e)[:80]}
        return status

    def xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_1(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = None
        for name in self.machine_names:
            try:
                client = self._get_client(name)
                status[name] = client.get_queue_status()
            except Exception as e:
                status[name] = {"error": str(e)[:80]}
        return status

    def xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_2(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = {}
        for name in self.machine_names:
            try:
                client = None
                status[name] = client.get_queue_status()
            except Exception as e:
                status[name] = {"error": str(e)[:80]}
        return status

    def xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_3(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = {}
        for name in self.machine_names:
            try:
                client = self._get_client(None)
                status[name] = client.get_queue_status()
            except Exception as e:
                status[name] = {"error": str(e)[:80]}
        return status

    def xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_4(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = {}
        for name in self.machine_names:
            try:
                client = self._get_client(name)
                status[name] = None
            except Exception as e:
                status[name] = {"error": str(e)[:80]}
        return status

    def xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_5(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = {}
        for name in self.machine_names:
            try:
                client = self._get_client(name)
                status[name] = client.get_queue_status()
            except Exception as e:
                status[name] = None
        return status

    def xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_6(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = {}
        for name in self.machine_names:
            try:
                client = self._get_client(name)
                status[name] = client.get_queue_status()
            except Exception as e:
                status[name] = {"XXerrorXX": str(e)[:80]}
        return status

    def xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_7(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = {}
        for name in self.machine_names:
            try:
                client = self._get_client(name)
                status[name] = client.get_queue_status()
            except Exception as e:
                status[name] = {"ERROR": str(e)[:80]}
        return status

    def xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_8(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = {}
        for name in self.machine_names:
            try:
                client = self._get_client(name)
                status[name] = client.get_queue_status()
            except Exception as e:
                status[name] = {"error": str(None)[:80]}
        return status

    def xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_9(self) -> dict[str, dict[str, Any]]:
        """聚合所有纳管机器的队列状态。

        Returns:
            {machine_name: queue_status_dict} 映射
        """
        status = {}
        for name in self.machine_names:
            try:
                client = self._get_client(name)
                status[name] = client.get_queue_status()
            except Exception as e:
                status[name] = {"error": str(e)[:81]}
        return status

    @_mutmut_mutated(mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut)
    def get_submit_stats(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, 0),
                "fail": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_orig(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, 0),
                "fail": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_1(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "XXsubmitXX": self._submit_count.get(name, 0),
                "fail": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_2(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "SUBMIT": self._submit_count.get(name, 0),
                "fail": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_3(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(None, 0),
                "fail": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_4(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, None),
                "fail": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_5(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(0),
                "fail": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_6(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, ),
                "fail": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_7(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, 1),
                "fail": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_8(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, 0),
                "XXfailXX": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_9(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, 0),
                "FAIL": self._fail_count.get(name, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_10(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, 0),
                "fail": self._fail_count.get(None, 0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_11(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, 0),
                "fail": self._fail_count.get(name, None),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_12(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, 0),
                "fail": self._fail_count.get(0),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_13(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, 0),
                "fail": self._fail_count.get(name, ),
            }
            for name in self.machine_names
        }

    def xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_14(self) -> dict[str, dict[str, int]]:
        """返回各机器的真机提交统计。

        Returns:
            {machine_name: {"submit": n, "fail": m}} 映射
        """
        return {
            name: {
                "submit": self._submit_count.get(name, 0),
                "fail": self._fail_count.get(name, 1),
            }
            for name in self.machine_names
        }

    @_mutmut_mutated(mutants_xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut)
    def as_client_map(self) -> dict[str, CqlibTianyanClient]:
        """返回 {machine_name: client} 映射，便于注入 env.attach_real_clients。

        注意：此方法会触发所有纳管机器的客户端懒加载。
        """
        for name in self.machine_names:
            self._get_client(name)
        return dict(self._clients)

    def xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut_orig(self) -> dict[str, CqlibTianyanClient]:
        """返回 {machine_name: client} 映射，便于注入 env.attach_real_clients。

        注意：此方法会触发所有纳管机器的客户端懒加载。
        """
        for name in self.machine_names:
            self._get_client(name)
        return dict(self._clients)

    def xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut_1(self) -> dict[str, CqlibTianyanClient]:
        """返回 {machine_name: client} 映射，便于注入 env.attach_real_clients。

        注意：此方法会触发所有纳管机器的客户端懒加载。
        """
        for name in self.machine_names:
            self._get_client(None)
        return dict(self._clients)

    def xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut_2(self) -> dict[str, CqlibTianyanClient]:
        """返回 {machine_name: client} 映射，便于注入 env.attach_real_clients。

        注意：此方法会触发所有纳管机器的客户端懒加载。
        """
        for name in self.machine_names:
            self._get_client(name)
        return dict(None)

mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['_mutmut_orig'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_1'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_2'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_3'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_4'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_5'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_6'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_7'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_8'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_9'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_10'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_11'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_12'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_12 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_13'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_13 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_14'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_14 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_15'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_15 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_16'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_16 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_17'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_17 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_18'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_18 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ__init____mutmut['xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_19'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ__init____mutmut_19 # type: ignore # mutmut generated

mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['_mutmut_orig'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_1'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_2'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_3'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_4'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_5'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_6'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_7'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_8'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_9'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut['xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_10'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁ_get_client__mutmut_10 # type: ignore # mutmut generated

mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['_mutmut_orig'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_1'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_2'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_3'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_4'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_5'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_6'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_7'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_8'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_9'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_10'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_11'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_12'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_13'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_14'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_15'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_16'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_17'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_18'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_18 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_19'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_19 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_20'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_20 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_21'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_21 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_22'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_22 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_23'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_23 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_24'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_24 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_25'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_25 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_26'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_26 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_27'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_27 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_28'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_28 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_29'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_29 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut['xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_30'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁsubmit_to_machine__mutmut_30 # type: ignore # mutmut generated

mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut['_mutmut_orig'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut['xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_1'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut['xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_2'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut['xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_3'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut['xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_4'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut['xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_5'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut['xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_6'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut['xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_7'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut['xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_8'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut['xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_9'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_all_status__mutmut_9 # type: ignore # mutmut generated

mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['_mutmut_orig'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_1'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_2'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_3'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_4'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_5'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_6'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_7'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_8'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_9'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_10'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_11'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_12'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_13'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut['xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_14'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁget_submit_stats__mutmut_14 # type: ignore # mutmut generated

mutants_xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut['_mutmut_orig'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut['xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut_1'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut['xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut_2'] = MultiMachineCqlibCoordinator.xǁMultiMachineCqlibCoordinatorǁas_client_map__mutmut_2 # type: ignore # mutmut generated
mutants_x_create_multi_machine_clients__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_create_multi_machine_clients__mutmut)
def create_multi_machine_clients(
    login_key: str,
    machine_names: list[str],
) -> dict[str, CqlibTianyanClient]:
    """工厂函数：为每台机器创建独立的 cqlib 客户端。

    Args:
        login_key    : 天衍云 API Key
        machine_names: 机器名列表

    Returns:
        {machine_name: CqlibTianyanClient} 映射，可直接传给 env.attach_real_clients
    """
    return {
        name: CqlibTianyanClient(
            login_key=login_key,
            machine_name=name,
            auto_retry_machine=False,
        )
        for name in machine_names
    }


def x_create_multi_machine_clients__mutmut_orig(
    login_key: str,
    machine_names: list[str],
) -> dict[str, CqlibTianyanClient]:
    """工厂函数：为每台机器创建独立的 cqlib 客户端。

    Args:
        login_key    : 天衍云 API Key
        machine_names: 机器名列表

    Returns:
        {machine_name: CqlibTianyanClient} 映射，可直接传给 env.attach_real_clients
    """
    return {
        name: CqlibTianyanClient(
            login_key=login_key,
            machine_name=name,
            auto_retry_machine=False,
        )
        for name in machine_names
    }


def x_create_multi_machine_clients__mutmut_1(
    login_key: str,
    machine_names: list[str],
) -> dict[str, CqlibTianyanClient]:
    """工厂函数：为每台机器创建独立的 cqlib 客户端。

    Args:
        login_key    : 天衍云 API Key
        machine_names: 机器名列表

    Returns:
        {machine_name: CqlibTianyanClient} 映射，可直接传给 env.attach_real_clients
    """
    return {
        name: CqlibTianyanClient(
            login_key=None,
            machine_name=name,
            auto_retry_machine=False,
        )
        for name in machine_names
    }


def x_create_multi_machine_clients__mutmut_2(
    login_key: str,
    machine_names: list[str],
) -> dict[str, CqlibTianyanClient]:
    """工厂函数：为每台机器创建独立的 cqlib 客户端。

    Args:
        login_key    : 天衍云 API Key
        machine_names: 机器名列表

    Returns:
        {machine_name: CqlibTianyanClient} 映射，可直接传给 env.attach_real_clients
    """
    return {
        name: CqlibTianyanClient(
            login_key=login_key,
            machine_name=None,
            auto_retry_machine=False,
        )
        for name in machine_names
    }


def x_create_multi_machine_clients__mutmut_3(
    login_key: str,
    machine_names: list[str],
) -> dict[str, CqlibTianyanClient]:
    """工厂函数：为每台机器创建独立的 cqlib 客户端。

    Args:
        login_key    : 天衍云 API Key
        machine_names: 机器名列表

    Returns:
        {machine_name: CqlibTianyanClient} 映射，可直接传给 env.attach_real_clients
    """
    return {
        name: CqlibTianyanClient(
            login_key=login_key,
            machine_name=name,
            auto_retry_machine=None,
        )
        for name in machine_names
    }


def x_create_multi_machine_clients__mutmut_4(
    login_key: str,
    machine_names: list[str],
) -> dict[str, CqlibTianyanClient]:
    """工厂函数：为每台机器创建独立的 cqlib 客户端。

    Args:
        login_key    : 天衍云 API Key
        machine_names: 机器名列表

    Returns:
        {machine_name: CqlibTianyanClient} 映射，可直接传给 env.attach_real_clients
    """
    return {
        name: CqlibTianyanClient(
            machine_name=name,
            auto_retry_machine=False,
        )
        for name in machine_names
    }


def x_create_multi_machine_clients__mutmut_5(
    login_key: str,
    machine_names: list[str],
) -> dict[str, CqlibTianyanClient]:
    """工厂函数：为每台机器创建独立的 cqlib 客户端。

    Args:
        login_key    : 天衍云 API Key
        machine_names: 机器名列表

    Returns:
        {machine_name: CqlibTianyanClient} 映射，可直接传给 env.attach_real_clients
    """
    return {
        name: CqlibTianyanClient(
            login_key=login_key,
            auto_retry_machine=False,
        )
        for name in machine_names
    }


def x_create_multi_machine_clients__mutmut_6(
    login_key: str,
    machine_names: list[str],
) -> dict[str, CqlibTianyanClient]:
    """工厂函数：为每台机器创建独立的 cqlib 客户端。

    Args:
        login_key    : 天衍云 API Key
        machine_names: 机器名列表

    Returns:
        {machine_name: CqlibTianyanClient} 映射，可直接传给 env.attach_real_clients
    """
    return {
        name: CqlibTianyanClient(
            login_key=login_key,
            machine_name=name,
            )
        for name in machine_names
    }


def x_create_multi_machine_clients__mutmut_7(
    login_key: str,
    machine_names: list[str],
) -> dict[str, CqlibTianyanClient]:
    """工厂函数：为每台机器创建独立的 cqlib 客户端。

    Args:
        login_key    : 天衍云 API Key
        machine_names: 机器名列表

    Returns:
        {machine_name: CqlibTianyanClient} 映射，可直接传给 env.attach_real_clients
    """
    return {
        name: CqlibTianyanClient(
            login_key=login_key,
            machine_name=name,
            auto_retry_machine=True,
        )
        for name in machine_names
    }

mutants_x_create_multi_machine_clients__mutmut['_mutmut_orig'] = x_create_multi_machine_clients__mutmut_orig # type: ignore # mutmut generated
mutants_x_create_multi_machine_clients__mutmut['x_create_multi_machine_clients__mutmut_1'] = x_create_multi_machine_clients__mutmut_1 # type: ignore # mutmut generated
mutants_x_create_multi_machine_clients__mutmut['x_create_multi_machine_clients__mutmut_2'] = x_create_multi_machine_clients__mutmut_2 # type: ignore # mutmut generated
mutants_x_create_multi_machine_clients__mutmut['x_create_multi_machine_clients__mutmut_3'] = x_create_multi_machine_clients__mutmut_3 # type: ignore # mutmut generated
mutants_x_create_multi_machine_clients__mutmut['x_create_multi_machine_clients__mutmut_4'] = x_create_multi_machine_clients__mutmut_4 # type: ignore # mutmut generated
mutants_x_create_multi_machine_clients__mutmut['x_create_multi_machine_clients__mutmut_5'] = x_create_multi_machine_clients__mutmut_5 # type: ignore # mutmut generated
mutants_x_create_multi_machine_clients__mutmut['x_create_multi_machine_clients__mutmut_6'] = x_create_multi_machine_clients__mutmut_6 # type: ignore # mutmut generated
mutants_x_create_multi_machine_clients__mutmut['x_create_multi_machine_clients__mutmut_7'] = x_create_multi_machine_clients__mutmut_7 # type: ignore # mutmut generated
