"""
统一异常层次结构模块
Unified Exception Hierarchy Module

为整个 quantum-rl-scheduler 系统提供统一的异常基类与具体异常类型。
所有自定义异常均派生自 QuantumSchedulerError，携带错误码（code）与
可重试标志（retryable），便于上层（熔断器、重试器、API 客户端）统一处理。
"""

__all__ = [
    "CircuitOpenError",
    "ConfigurationError",
    "QuantumAnnealingError",
    "QuantumSchedulerError",
    "ResourceExhaustedError",
    "SchedulingError",
    "TaskParseError",
    "TianyanAPIError",
]


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁQuantumSchedulerErrorǁ__init____mutmut: MutantDict = {}  # type: ignore


class QuantumSchedulerError(Exception):
    """系统基础异常

    所有 quantum-rl-scheduler 自定义异常的基类，携带错误码与可重试标志，
    便于熔断器、重试器等上层组件统一决策。

    Args:
        message: 异常描述信息
        code: 错误码（关键字参数，默认 "UNKNOWN"）
        retryable: 该异常是否可重试（关键字参数，默认 False）
    """

    @_mutmut_mutated(mutants_xǁQuantumSchedulerErrorǁ__init____mutmut)
    def __init__(self, message: str, *, code: str = "UNKNOWN", retryable: bool = False) -> None:
        self.code = code
        self.retryable = retryable
        super().__init__(message)

    def xǁQuantumSchedulerErrorǁ__init____mutmut_orig(self, message: str, *, code: str = "UNKNOWN", retryable: bool = False) -> None:
        self.code = code
        self.retryable = retryable
        super().__init__(message)

    def xǁQuantumSchedulerErrorǁ__init____mutmut_1(self, message: str, *, code: str = "XXUNKNOWNXX", retryable: bool = False) -> None:
        self.code = code
        self.retryable = retryable
        super().__init__(message)

    def xǁQuantumSchedulerErrorǁ__init____mutmut_2(self, message: str, *, code: str = "unknown", retryable: bool = False) -> None:
        self.code = code
        self.retryable = retryable
        super().__init__(message)

    def xǁQuantumSchedulerErrorǁ__init____mutmut_3(self, message: str, *, code: str = "UNKNOWN", retryable: bool = True) -> None:
        self.code = code
        self.retryable = retryable
        super().__init__(message)

    def xǁQuantumSchedulerErrorǁ__init____mutmut_4(self, message: str, *, code: str = "UNKNOWN", retryable: bool = False) -> None:
        self.code = None
        self.retryable = retryable
        super().__init__(message)

    def xǁQuantumSchedulerErrorǁ__init____mutmut_5(self, message: str, *, code: str = "UNKNOWN", retryable: bool = False) -> None:
        self.code = code
        self.retryable = None
        super().__init__(message)

    def xǁQuantumSchedulerErrorǁ__init____mutmut_6(self, message: str, *, code: str = "UNKNOWN", retryable: bool = False) -> None:
        self.code = code
        self.retryable = retryable
        super().__init__(None)

mutants_xǁQuantumSchedulerErrorǁ__init____mutmut['_mutmut_orig'] = QuantumSchedulerError.xǁQuantumSchedulerErrorǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁQuantumSchedulerErrorǁ__init____mutmut['xǁQuantumSchedulerErrorǁ__init____mutmut_1'] = QuantumSchedulerError.xǁQuantumSchedulerErrorǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁQuantumSchedulerErrorǁ__init____mutmut['xǁQuantumSchedulerErrorǁ__init____mutmut_2'] = QuantumSchedulerError.xǁQuantumSchedulerErrorǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁQuantumSchedulerErrorǁ__init____mutmut['xǁQuantumSchedulerErrorǁ__init____mutmut_3'] = QuantumSchedulerError.xǁQuantumSchedulerErrorǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁQuantumSchedulerErrorǁ__init____mutmut['xǁQuantumSchedulerErrorǁ__init____mutmut_4'] = QuantumSchedulerError.xǁQuantumSchedulerErrorǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁQuantumSchedulerErrorǁ__init____mutmut['xǁQuantumSchedulerErrorǁ__init____mutmut_5'] = QuantumSchedulerError.xǁQuantumSchedulerErrorǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁQuantumSchedulerErrorǁ__init____mutmut['xǁQuantumSchedulerErrorǁ__init____mutmut_6'] = QuantumSchedulerError.xǁQuantumSchedulerErrorǁ__init____mutmut_6 # type: ignore # mutmut generated


class TianyanAPIError(QuantumSchedulerError):
    """天衍云 API 异常

    用于天衍云平台 API 调用失败的场景，如鉴权失败、请求超时、服务端错误等。
    """


class CircuitOpenError(QuantumSchedulerError):
    """熔断器打开异常

    当熔断器处于 OPEN 状态且尚未到达恢复超时时间时，调用将被拒绝并抛出此异常。
    """


class ConfigurationError(QuantumSchedulerError):
    """配置错误（不可重试）

    用于配置文件缺失、字段非法、环境变量未设置等场景，通常不可通过重试解决。
    """


class TaskParseError(QuantumSchedulerError):
    """任务解析错误

    用于 QASM 电路解析失败、任务字段缺失或格式非法等场景。
    """


class SchedulingError(QuantumSchedulerError):
    """调度错误

    用于调度引擎内部状态错误、无可用机器、动作非法等场景。
    """


class QuantumAnnealingError(QuantumSchedulerError):
    """量子退火错误

    用于 QUBO 矩阵构造失败、退火求解异常、结果不收敛等场景。
    """


class ResourceExhaustedError(QuantumSchedulerError):
    """资源耗尽错误

    用于量子比特、机器队列、连接池等资源耗尽，无法接受新任务的场景。
    """
