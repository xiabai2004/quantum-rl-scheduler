"""
熔断器模块
Circuit Breaker Module

实现熔断器模式（Circuit Breaker Pattern）：当连续调用失败达到阈值时
自动熔断，避免对故障服务的持续压力；经过恢复超时后进入 HALF_OPEN
状态放行一次试探性调用，根据结果决定恢复或继续熔断。
"""

import time
from collections.abc import Callable
from enum import Enum
from typing import Any, TypeVar

from src.exceptions import CircuitOpenError

__all__ = ["CircuitBreaker", "CircuitState"]

T = TypeVar("T")


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class CircuitState(Enum):
    """熔断器状态枚举

    Attributes:
        CLOSED: 正常放行
        OPEN: 熔断拒绝
        HALF_OPEN: 试探性恢复
    """

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"
mutants_xǁCircuitBreakerǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁCircuitBreakerǁcall__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCircuitBreakerǁreset__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCircuitBreakerǁis_available__mutmut: MutantDict = {}  # type: ignore


class CircuitBreaker:
    """熔断器

    在函数调用外层包裹熔断逻辑：

    - CLOSED：正常放行；失败时累加计数，达到阈值转为 OPEN
    - OPEN：拒绝调用并抛出 CircuitOpenError；超过 recovery_timeout 后转为 HALF_OPEN
    - HALF_OPEN：放行一次试探性调用；成功则重置为 CLOSED，失败则重回 OPEN

    Args:
        failure_threshold: 连续失败触发熔断的阈值
        recovery_timeout: OPEN 状态恢复到 HALF_OPEN 的等待秒数
    """

    @_mutmut_mutated(mutants_xǁCircuitBreakerǁ__init____mutmut)
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.last_failure_time: float = 0.0

    def xǁCircuitBreakerǁ__init____mutmut_orig(self, failure_threshold: int = 5, recovery_timeout: float = 60.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.last_failure_time: float = 0.0

    def xǁCircuitBreakerǁ__init____mutmut_1(self, failure_threshold: int = 6, recovery_timeout: float = 60.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.last_failure_time: float = 0.0

    def xǁCircuitBreakerǁ__init____mutmut_2(self, failure_threshold: int = 5, recovery_timeout: float = 61.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.last_failure_time: float = 0.0

    def xǁCircuitBreakerǁ__init____mutmut_3(self, failure_threshold: int = 5, recovery_timeout: float = 60.0) -> None:
        self.failure_threshold = None
        self.recovery_timeout = recovery_timeout
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.last_failure_time: float = 0.0

    def xǁCircuitBreakerǁ__init____mutmut_4(self, failure_threshold: int = 5, recovery_timeout: float = 60.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = None
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.last_failure_time: float = 0.0

    def xǁCircuitBreakerǁ__init____mutmut_5(self, failure_threshold: int = 5, recovery_timeout: float = 60.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state: CircuitState = None
        self.failure_count: int = 0
        self.last_failure_time: float = 0.0

    def xǁCircuitBreakerǁ__init____mutmut_6(self, failure_threshold: int = 5, recovery_timeout: float = 60.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = None
        self.last_failure_time: float = 0.0

    def xǁCircuitBreakerǁ__init____mutmut_7(self, failure_threshold: int = 5, recovery_timeout: float = 60.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 1
        self.last_failure_time: float = 0.0

    def xǁCircuitBreakerǁ__init____mutmut_8(self, failure_threshold: int = 5, recovery_timeout: float = 60.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.last_failure_time: float = None

    def xǁCircuitBreakerǁ__init____mutmut_9(self, failure_threshold: int = 5, recovery_timeout: float = 60.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state: CircuitState = CircuitState.CLOSED
        self.failure_count: int = 0
        self.last_failure_time: float = 1.0

    @_mutmut_mutated(mutants_xǁCircuitBreakerǁcall__mutmut)
    def call(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_orig(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_1(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state != CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_2(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() + self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_3(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time > self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_4(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = None
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_5(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    None,
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_6(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code=None,
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_7(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=None,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_8(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_9(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_10(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_11(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "XX熔断器处于 OPEN 状态，拒绝调用XX",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_12(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 open 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_13(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="XXCIRCUIT_OPENXX",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_14(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="circuit_open",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_15(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=False,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_16(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = None
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_17(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(**kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_18(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, )
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_19(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count = 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_20(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count -= 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_21(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 2
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_22(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = None
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_23(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state != CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_24(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = None
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_25(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED or self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_26(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state != CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_27(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count > self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_28(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = None
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_29(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state != CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_30(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state != CircuitState.CLOSED:
            self.failure_count = 0
        return result

    def xǁCircuitBreakerǁcall__mutmut_31(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = None
        return result

    def xǁCircuitBreakerǁcall__mutmut_32(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """通过熔断器执行函数

        Args:
            func: 待调用的可调用对象
            *args: 透传给 func 的位置参数
            **kwargs: 透传给 func 的关键字参数

        Returns:
            func 的返回值

        Raises:
            CircuitOpenError: 熔断器处于 OPEN 状态且未到恢复超时
        """
        # OPEN 状态：判断是否已过恢复超时
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                # 进入 HALF_OPEN，放行一次试探性调用
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(
                    "熔断器处于 OPEN 状态，拒绝调用",
                    code="CIRCUIT_OPEN",
                    retryable=True,
                )

        try:
            result = func(*args, **kwargs)
        except Exception:
            # 失败：累加计数并更新失败时间
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                # 试探性调用失败，重回 OPEN
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise

        # 成功：HALF_OPEN 试探通过则重置，CLOSED 则清零连续失败计数
        if self.state == CircuitState.HALF_OPEN:
            self.reset()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 1
        return result

    @_mutmut_mutated(mutants_xǁCircuitBreakerǁreset__mutmut)
    def reset(self) -> None:
        """手动重置熔断器为 CLOSED 状态并清零失败计数"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    def xǁCircuitBreakerǁreset__mutmut_orig(self) -> None:
        """手动重置熔断器为 CLOSED 状态并清零失败计数"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    def xǁCircuitBreakerǁreset__mutmut_1(self) -> None:
        """手动重置熔断器为 CLOSED 状态并清零失败计数"""
        self.state = None
        self.failure_count = 0
        self.last_failure_time = 0.0

    def xǁCircuitBreakerǁreset__mutmut_2(self) -> None:
        """手动重置熔断器为 CLOSED 状态并清零失败计数"""
        self.state = CircuitState.CLOSED
        self.failure_count = None
        self.last_failure_time = 0.0

    def xǁCircuitBreakerǁreset__mutmut_3(self) -> None:
        """手动重置熔断器为 CLOSED 状态并清零失败计数"""
        self.state = CircuitState.CLOSED
        self.failure_count = 1
        self.last_failure_time = 0.0

    def xǁCircuitBreakerǁreset__mutmut_4(self) -> None:
        """手动重置熔断器为 CLOSED 状态并清零失败计数"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

    def xǁCircuitBreakerǁreset__mutmut_5(self) -> None:
        """手动重置熔断器为 CLOSED 状态并清零失败计数"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 1.0

    @_mutmut_mutated(mutants_xǁCircuitBreakerǁis_available__mutmut)
    def is_available(self) -> bool:
        """判断熔断器当前是否放行调用

        Returns:
            True 表示调用可放行（CLOSED / HALF_OPEN，或 OPEN 已过恢复超时）
        """
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.HALF_OPEN:
            return True
        # OPEN 状态：判断是否已过恢复超时
        return time.monotonic() - self.last_failure_time >= self.recovery_timeout

    def xǁCircuitBreakerǁis_available__mutmut_orig(self) -> bool:
        """判断熔断器当前是否放行调用

        Returns:
            True 表示调用可放行（CLOSED / HALF_OPEN，或 OPEN 已过恢复超时）
        """
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.HALF_OPEN:
            return True
        # OPEN 状态：判断是否已过恢复超时
        return time.monotonic() - self.last_failure_time >= self.recovery_timeout

    def xǁCircuitBreakerǁis_available__mutmut_1(self) -> bool:
        """判断熔断器当前是否放行调用

        Returns:
            True 表示调用可放行（CLOSED / HALF_OPEN，或 OPEN 已过恢复超时）
        """
        if self.state != CircuitState.CLOSED:
            return True
        if self.state == CircuitState.HALF_OPEN:
            return True
        # OPEN 状态：判断是否已过恢复超时
        return time.monotonic() - self.last_failure_time >= self.recovery_timeout

    def xǁCircuitBreakerǁis_available__mutmut_2(self) -> bool:
        """判断熔断器当前是否放行调用

        Returns:
            True 表示调用可放行（CLOSED / HALF_OPEN，或 OPEN 已过恢复超时）
        """
        if self.state == CircuitState.CLOSED:
            return False
        if self.state == CircuitState.HALF_OPEN:
            return True
        # OPEN 状态：判断是否已过恢复超时
        return time.monotonic() - self.last_failure_time >= self.recovery_timeout

    def xǁCircuitBreakerǁis_available__mutmut_3(self) -> bool:
        """判断熔断器当前是否放行调用

        Returns:
            True 表示调用可放行（CLOSED / HALF_OPEN，或 OPEN 已过恢复超时）
        """
        if self.state == CircuitState.CLOSED:
            return True
        if self.state != CircuitState.HALF_OPEN:
            return True
        # OPEN 状态：判断是否已过恢复超时
        return time.monotonic() - self.last_failure_time >= self.recovery_timeout

    def xǁCircuitBreakerǁis_available__mutmut_4(self) -> bool:
        """判断熔断器当前是否放行调用

        Returns:
            True 表示调用可放行（CLOSED / HALF_OPEN，或 OPEN 已过恢复超时）
        """
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.HALF_OPEN:
            return False
        # OPEN 状态：判断是否已过恢复超时
        return time.monotonic() - self.last_failure_time >= self.recovery_timeout

    def xǁCircuitBreakerǁis_available__mutmut_5(self) -> bool:
        """判断熔断器当前是否放行调用

        Returns:
            True 表示调用可放行（CLOSED / HALF_OPEN，或 OPEN 已过恢复超时）
        """
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.HALF_OPEN:
            return True
        # OPEN 状态：判断是否已过恢复超时
        return time.monotonic() + self.last_failure_time >= self.recovery_timeout

    def xǁCircuitBreakerǁis_available__mutmut_6(self) -> bool:
        """判断熔断器当前是否放行调用

        Returns:
            True 表示调用可放行（CLOSED / HALF_OPEN，或 OPEN 已过恢复超时）
        """
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.HALF_OPEN:
            return True
        # OPEN 状态：判断是否已过恢复超时
        return time.monotonic() - self.last_failure_time > self.recovery_timeout

mutants_xǁCircuitBreakerǁ__init____mutmut['_mutmut_orig'] = CircuitBreaker.xǁCircuitBreakerǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁ__init____mutmut['xǁCircuitBreakerǁ__init____mutmut_1'] = CircuitBreaker.xǁCircuitBreakerǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁ__init____mutmut['xǁCircuitBreakerǁ__init____mutmut_2'] = CircuitBreaker.xǁCircuitBreakerǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁ__init____mutmut['xǁCircuitBreakerǁ__init____mutmut_3'] = CircuitBreaker.xǁCircuitBreakerǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁ__init____mutmut['xǁCircuitBreakerǁ__init____mutmut_4'] = CircuitBreaker.xǁCircuitBreakerǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁ__init____mutmut['xǁCircuitBreakerǁ__init____mutmut_5'] = CircuitBreaker.xǁCircuitBreakerǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁ__init____mutmut['xǁCircuitBreakerǁ__init____mutmut_6'] = CircuitBreaker.xǁCircuitBreakerǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁ__init____mutmut['xǁCircuitBreakerǁ__init____mutmut_7'] = CircuitBreaker.xǁCircuitBreakerǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁ__init____mutmut['xǁCircuitBreakerǁ__init____mutmut_8'] = CircuitBreaker.xǁCircuitBreakerǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁ__init____mutmut['xǁCircuitBreakerǁ__init____mutmut_9'] = CircuitBreaker.xǁCircuitBreakerǁ__init____mutmut_9 # type: ignore # mutmut generated

mutants_xǁCircuitBreakerǁcall__mutmut['_mutmut_orig'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_1'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_2'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_3'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_4'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_5'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_6'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_7'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_8'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_9'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_10'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_11'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_12'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_13'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_14'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_15'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_16'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_17'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_18'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_19'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_20'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_21'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_22'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_23'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_24'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_25'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_26'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_27'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_28'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_29'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_30'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_31'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁcall__mutmut['xǁCircuitBreakerǁcall__mutmut_32'] = CircuitBreaker.xǁCircuitBreakerǁcall__mutmut_32 # type: ignore # mutmut generated

mutants_xǁCircuitBreakerǁreset__mutmut['_mutmut_orig'] = CircuitBreaker.xǁCircuitBreakerǁreset__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁreset__mutmut['xǁCircuitBreakerǁreset__mutmut_1'] = CircuitBreaker.xǁCircuitBreakerǁreset__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁreset__mutmut['xǁCircuitBreakerǁreset__mutmut_2'] = CircuitBreaker.xǁCircuitBreakerǁreset__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁreset__mutmut['xǁCircuitBreakerǁreset__mutmut_3'] = CircuitBreaker.xǁCircuitBreakerǁreset__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁreset__mutmut['xǁCircuitBreakerǁreset__mutmut_4'] = CircuitBreaker.xǁCircuitBreakerǁreset__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁreset__mutmut['xǁCircuitBreakerǁreset__mutmut_5'] = CircuitBreaker.xǁCircuitBreakerǁreset__mutmut_5 # type: ignore # mutmut generated

mutants_xǁCircuitBreakerǁis_available__mutmut['_mutmut_orig'] = CircuitBreaker.xǁCircuitBreakerǁis_available__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁis_available__mutmut['xǁCircuitBreakerǁis_available__mutmut_1'] = CircuitBreaker.xǁCircuitBreakerǁis_available__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁis_available__mutmut['xǁCircuitBreakerǁis_available__mutmut_2'] = CircuitBreaker.xǁCircuitBreakerǁis_available__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁis_available__mutmut['xǁCircuitBreakerǁis_available__mutmut_3'] = CircuitBreaker.xǁCircuitBreakerǁis_available__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁis_available__mutmut['xǁCircuitBreakerǁis_available__mutmut_4'] = CircuitBreaker.xǁCircuitBreakerǁis_available__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁis_available__mutmut['xǁCircuitBreakerǁis_available__mutmut_5'] = CircuitBreaker.xǁCircuitBreakerǁis_available__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCircuitBreakerǁis_available__mutmut['xǁCircuitBreakerǁis_available__mutmut_6'] = CircuitBreaker.xǁCircuitBreakerǁis_available__mutmut_6 # type: ignore # mutmut generated
