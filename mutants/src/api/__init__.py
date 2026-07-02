"""
src.api 包初始化模块
支持三种后端：Mock / REST / cqlib（真机优先）
"""

import os
from typing import Any

from src.api.mock_client import MockTianyanClient, create_tianyan_client
from src.api.tianyan_client import CircuitState, TianyanAPIError, TianyanClient
from src.api.tianyan_cqlib import (
    CqlibTianyanClient,
    MultiMachineCqlibCoordinator,
    create_multi_machine_clients,
)

__all__ = [
    "CircuitState",
    "CqlibTianyanClient",
    "MockTianyanClient",
    "MultiMachineCqlibCoordinator",
    "TianyanAPIError",
    "TianyanClient",
    "create_multi_machine_clients",
    "create_tianyan_client",
    "get_client",
    "get_cqlib_client",
]


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_get_cqlib_client__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_get_cqlib_client__mutmut)
def get_cqlib_client(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_orig(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_1(machine_name: str = "XXtianyan_sXX") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_2(machine_name: str = "TIANYAN_S") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_3(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = None
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_4(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv(None, "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_5(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", None)
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_6(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_7(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", )
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_8(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("XXTIANYAN_API_KEYXX", "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_9(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("tianyan_api_key", "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_10(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "XXXX")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_11(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_12(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError(None)
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_13(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError("XX未设置 TIANYAN_API_KEY 环境变量XX")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_14(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError("未设置 tianyan_api_key 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=machine_name)


def x_get_cqlib_client__mutmut_15(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=None, machine_name=machine_name)


def x_get_cqlib_client__mutmut_16(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, machine_name=None)


def x_get_cqlib_client__mutmut_17(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(machine_name=machine_name)


def x_get_cqlib_client__mutmut_18(machine_name: str = "tianyan_s") -> CqlibTianyanClient:
    """获取 cqlib 真机客户端

    从环境变量 TIANYAN_API_KEY 读取密钥，直接连接天衍云超导真机。

    Args:
        machine_name: 量子计算机名称（默认 tianyan_s）

    Returns:
        CqlibTianyanClient 实例
    """
    api_key = os.getenv("TIANYAN_API_KEY", "")
    if not api_key:
        raise ValueError("未设置 TIANYAN_API_KEY 环境变量")
    return CqlibTianyanClient(login_key=api_key, )

mutants_x_get_cqlib_client__mutmut['_mutmut_orig'] = x_get_cqlib_client__mutmut_orig # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_1'] = x_get_cqlib_client__mutmut_1 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_2'] = x_get_cqlib_client__mutmut_2 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_3'] = x_get_cqlib_client__mutmut_3 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_4'] = x_get_cqlib_client__mutmut_4 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_5'] = x_get_cqlib_client__mutmut_5 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_6'] = x_get_cqlib_client__mutmut_6 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_7'] = x_get_cqlib_client__mutmut_7 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_8'] = x_get_cqlib_client__mutmut_8 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_9'] = x_get_cqlib_client__mutmut_9 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_10'] = x_get_cqlib_client__mutmut_10 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_11'] = x_get_cqlib_client__mutmut_11 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_12'] = x_get_cqlib_client__mutmut_12 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_13'] = x_get_cqlib_client__mutmut_13 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_14'] = x_get_cqlib_client__mutmut_14 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_15'] = x_get_cqlib_client__mutmut_15 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_16'] = x_get_cqlib_client__mutmut_16 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_17'] = x_get_cqlib_client__mutmut_17 # type: ignore # mutmut generated
mutants_x_get_cqlib_client__mutmut['x_get_cqlib_client__mutmut_18'] = x_get_cqlib_client__mutmut_18 # type: ignore # mutmut generated
mutants_x_get_client__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_get_client__mutmut)
def get_client(mock_mode: bool | None = None) -> Any:
    """获取天衍云客户端（自动选择真实或 Mock 模式）

    优先读取顺序：
    1. 显式传参 mock_mode
    2. 环境变量 TIANYAN_MOCK_MODE
    3. 默认使用 Mock 模式

    Args:
        mock_mode: 是否使用 Mock 模式（None 表示自动检测）

    Returns:
        客户端实例
    """
    return create_tianyan_client(mock_mode=mock_mode)


def x_get_client__mutmut_orig(mock_mode: bool | None = None) -> Any:
    """获取天衍云客户端（自动选择真实或 Mock 模式）

    优先读取顺序：
    1. 显式传参 mock_mode
    2. 环境变量 TIANYAN_MOCK_MODE
    3. 默认使用 Mock 模式

    Args:
        mock_mode: 是否使用 Mock 模式（None 表示自动检测）

    Returns:
        客户端实例
    """
    return create_tianyan_client(mock_mode=mock_mode)


def x_get_client__mutmut_1(mock_mode: bool | None = None) -> Any:
    """获取天衍云客户端（自动选择真实或 Mock 模式）

    优先读取顺序：
    1. 显式传参 mock_mode
    2. 环境变量 TIANYAN_MOCK_MODE
    3. 默认使用 Mock 模式

    Args:
        mock_mode: 是否使用 Mock 模式（None 表示自动检测）

    Returns:
        客户端实例
    """
    return create_tianyan_client(mock_mode=None)

mutants_x_get_client__mutmut['_mutmut_orig'] = x_get_client__mutmut_orig # type: ignore # mutmut generated
mutants_x_get_client__mutmut['x_get_client__mutmut_1'] = x_get_client__mutmut_1 # type: ignore # mutmut generated
