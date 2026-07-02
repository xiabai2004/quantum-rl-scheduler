"""
多目标强化学习 (MORL) 奖励包装器
Multi-Objective RL Reward Wrapper for Quantum Scheduling

将 QuantumSchedulingEnv 的标量奖励分解为 3 个独立目标：
    1. 吞吐量目标 (throughput): 任务完成速率 = 单位时间完成的任务数
    2. 资源平衡目标 (balance):    量子/经典资源利用率的平衡度
    3. 服务质量目标 (quality):    用户等待时间

通过加权标量化 (Weighted Scalarization) 将多目标合并为标量奖励：
    reward = w[0] * throughput + w[1] * balance + w[2] * quality

每个目标的独立值通过 info["objectives"] 字典返回。

使用方式:
    from src.scheduler.env import QuantumSchedulingEnv
    from src.scheduler.multi_objective_env import MultiObjectiveRewardWrapper

    env = QuantumSchedulingEnv(max_qubits=20)
    mo_env = MultiObjectiveRewardWrapper(env, weights=[1.0, 0.5, 0.5])
    obs, info = mo_env.reset()
    obs, reward, terminated, truncated, info = mo_env.step(action)
    # info["objectives"] = {"throughput": ..., "balance": ..., "quality": ...}
"""

from typing import Any

import gymnasium as gym
import numpy as np

from src.scheduler.env import (
    MAX_WAIT_STEPS,
    QuantumSchedulingEnv,
)

# ---------------------------------------------------------------------------
# 多目标权重预设
# ---------------------------------------------------------------------------

# 预定义权重组合（对应不同调度偏好）
DEFAULT_WEIGHTS = {
    "throughput_heavy": [1.0, 0.5, 0.5],  # 偏吞吐量
    "balance_heavy": [0.5, 1.0, 0.5],  # 偏资源平衡
    "quality_heavy": [0.5, 0.5, 1.0],  # 偏服务质量
    "balanced": [1.0, 1.0, 1.0],  # 均衡
    "throughput_only": [1.0, 0.0, 0.0],  # 仅吞吐量
    "balance_only": [0.0, 1.0, 0.0],  # 仅平衡
    "quality_only": [0.0, 0.0, 1.0],  # 仅服务质量
}


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut: MutantDict = {}  # type: ignore


class MultiObjectiveRewardWrapper(gym.Wrapper):
    """
    多目标奖励包装器。

    将原始环境的标量奖励分解为 3 个独立目标：
        - throughput: 任务完成速率（0~1 归一化）
        - balance:    量子/经典资源利用率平衡度（-1~0）
        - quality:    用户等待时间服务质量（-1~0）

    通过加权标量化合并为标量奖励，同时通过 info dict 返回每个目标的独立值。

    Attributes:
        weights: 3 元素列表，对应 [throughput, balance, quality] 的权重
        env: 被包装的 QuantumSchedulingEnv
    """

    @_mutmut_mutated(mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut)
    def __init__(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_orig(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_1(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(None)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_2(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None or weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_3(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_4(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_5(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError(None)
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_6(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("XX不能同时指定 weights 和 weight_presetXX")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_7(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 WEIGHTS 和 WEIGHT_PRESET")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_8(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_9(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_10(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    None
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_11(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(None)}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_12(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = None
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_13(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(None)
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_14(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_15(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) == 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_16(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 4:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_17(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(None)
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_18(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = None
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_19(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(None)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_20(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = None  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_21(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [2.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_22(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 1.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_23(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 1.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = self._reset_mo_stats()

    def xǁMultiObjectiveRewardWrapperǁ__init____mutmut_24(
        self,
        env: QuantumSchedulingEnv,
        weights: list[float] | None = None,
        weight_preset: str | None = None,
    ):
        """
        初始化多目标奖励包装器。

        Args:
            env: QuantumSchedulingEnv 实例
            weights: 3 元素列表 [w_throughput, w_balance, w_quality]
            weight_preset: 预定义权重名称，如 "throughput_heavy"
                           weights 和 weight_preset 不能同时指定
        """
        super().__init__(env)
        if weights is not None and weight_preset is not None:
            raise ValueError("不能同时指定 weights 和 weight_preset")
        if weight_preset is not None:
            if weight_preset not in DEFAULT_WEIGHTS:
                raise ValueError(
                    f"未知权重预设 '{weight_preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}"
                )
            self._weights = list(DEFAULT_WEIGHTS[weight_preset])
        elif weights is not None:
            if len(weights) != 3:
                raise ValueError(f"weights 必须包含 3 个元素，实际: {len(weights)}")
            self._weights = list(weights)
        else:
            self._weights = [1.0, 0.5, 0.5]  # 默认偏吞吐量

        # 多目标累积统计（每 episode 重置）
        self._mo_stats = None

    # ------------------------------------------------------------------
    # 权重属性
    # ------------------------------------------------------------------

    @property
    def weights(self) -> list[float]:
        """返回当前权重 [w_throughput, w_balance, w_quality]."""
        return list(self._weights)

    @weights.setter
    def weights(self, value: list[float]) -> None:
        """
        运行时动态切换权重，无需重新训练。

        Args:
            value: 3 元素权重列表
        """
        if len(value) != 3:
            raise ValueError(f"weights 必须包含 3 个元素，实际: {len(value)}")
        self._weights = list(value)

    @property
    def weight_names(self) -> list[str]:
        """返回权重名称列表。"""
        return ["throughput", "balance", "quality"]

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    @_mutmut_mutated(mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut)
    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_orig(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_1(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = None
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_2(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=None, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_3(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=None)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_4(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_5(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, )
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_6(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = None
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_7(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = None
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_8(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["XXobjectivesXX"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_9(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["OBJECTIVES"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_10(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "XXthroughputXX": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_11(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "THROUGHPUT": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_12(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 1.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_13(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "XXbalanceXX": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_14(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "BALANCE": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_15(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 1.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_16(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "XXqualityXX": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_17(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "QUALITY": 0.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_18(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 1.0,
        }
        info["mo_weights"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_19(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = None
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_20(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["XXmo_weightsXX"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_21(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["MO_WEIGHTS"] = list(self._weights)
        return obs, info

    # ------------------------------------------------------------------
    # reset()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁreset__mutmut_22(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        重置环境并初始化多目标统计。

        Args:
            seed: 随机种子
            options: 额外选项

        Returns:
            observation: 状态向量
            info: 包含 objectives 初始化值的字典
        """
        obs, info = super().reset(seed=seed, options=options)
        self._mo_stats = self._reset_mo_stats()
        # 初始化时各目标为 0
        info["objectives"] = {
            "throughput": 0.0,
            "balance": 0.0,
            "quality": 0.0,
        }
        info["mo_weights"] = list(None)
        return obs, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    @_mutmut_mutated(mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut)
    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_orig(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_1(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = None

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_2(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(None)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_3(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = None
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_4(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(None)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_5(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = None
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_6(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = None

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_7(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] = throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_8(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] -= throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_9(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["XXtotal_throughputXX"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_10(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["TOTAL_THROUGHPUT"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_11(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] = balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_12(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] -= balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_13(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["XXtotal_balanceXX"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_14(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["TOTAL_BALANCE"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_15(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] = quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_16(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] -= quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_17(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["XXtotal_qualityXX"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_18(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["TOTAL_QUALITY"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_19(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] = 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_20(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] -= 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_21(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["XXstepsXX"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_22(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["STEPS"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_23(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 2

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_24(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = None

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_25(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance - self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_26(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput - self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_27(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] / throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_28(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[1] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_29(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] / balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_30(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[2] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_31(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] / quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_32(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[3] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_33(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = None
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_34(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["XXobjectivesXX"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_35(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["OBJECTIVES"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_36(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "XXthroughputXX": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_37(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "THROUGHPUT": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_38(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(None),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_39(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "XXbalanceXX": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_40(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "BALANCE": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_41(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(None),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_42(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "XXqualityXX": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_43(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "QUALITY": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_44(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(None),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_45(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = None
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_46(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["XXmo_weightsXX"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_47(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["MO_WEIGHTS"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_48(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(None)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_49(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = None
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_50(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["XXoriginal_rewardXX"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_51(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["ORIGINAL_REWARD"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_52(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(None)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_53(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = None
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_54(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["XXmo_rewardXX"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_55(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["MO_REWARD"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_56(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(None)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_57(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = None

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_58(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["XXmo_cumulativeXX"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_59(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["MO_CUMULATIVE"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_60(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "XXthroughputXX": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_61(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "THROUGHPUT": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_62(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(None),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_63(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["XXtotal_throughputXX"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_64(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["TOTAL_THROUGHPUT"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_65(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "XXbalanceXX": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_66(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "BALANCE": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_67(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(None),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_68(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["XXtotal_balanceXX"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_69(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["TOTAL_BALANCE"]),
            "quality": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_70(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "XXqualityXX": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_71(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "QUALITY": float(self._mo_stats["total_quality"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_72(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(None),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_73(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["XXtotal_qualityXX"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # step()
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁstep__mutmut_74(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """
        执行一步调度决策，计算多目标奖励。

        核心逻辑：
            1. 调用原始 env.step() 获取原始标量奖励
            2. 从当前环境状态中计算 3 个独立目标值
            3. 加权标量化：reward = w[0]*throughput + w[1]*balance + w[2]*quality
            4. 将独立目标值存入 info["objectives"]

        Args:
            action: 动作索引

        Returns:
            observation: 下一步状态
            reward: 加权标量化奖励
            terminated: 是否终止
            truncated: 是否截断
            info: 包含 objectives 和原始标量奖励的字典
        """
        # 先调用原始 step，获取原始奖励和基础 info
        # 注：原始 step 已计算了 env 内部的标量奖励，
        # 这里我们重新计算多目标，用多目标加权 reward 替代原始 reward
        orig_obs, orig_reward, terminated, truncated, info = self.env.step(action)

        # 计算 3 个独立目标值
        throughput = self._compute_throughput(info)
        balance = self._compute_balance()
        quality = self._compute_quality()

        # 累计统计
        self._mo_stats["total_throughput"] += throughput
        self._mo_stats["total_balance"] += balance
        self._mo_stats["total_quality"] += quality
        self._mo_stats["steps"] += 1

        # 加权标量化
        reward = (
            self._weights[0] * throughput + self._weights[1] * balance + self._weights[2] * quality
        )

        # 存入 info dict
        info["objectives"] = {
            "throughput": float(throughput),
            "balance": float(balance),
            "quality": float(quality),
        }
        info["mo_weights"] = list(self._weights)
        info["original_reward"] = float(orig_reward)
        info["mo_reward"] = float(reward)
        info["mo_cumulative"] = {
            "throughput": float(self._mo_stats["total_throughput"]),
            "balance": float(self._mo_stats["total_balance"]),
            "quality": float(self._mo_stats["TOTAL_QUALITY"]),
        }

        return orig_obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    @_mutmut_mutated(mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut)
    def _compute_throughput(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_orig(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_1(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = None
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_2(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 1.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_3(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = None  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_4(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None and env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_5(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_6(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled >= 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_7(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 1:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_8(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get(None, 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_9(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", None) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_10(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get(0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_11(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", ) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_12(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("XXtotal_scheduledXX", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_13(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("TOTAL_SCHEDULED", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_14(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 1) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_15(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) >= self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_16(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get(None, 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_17(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", None):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_18(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get(0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_19(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", ):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_20(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("XX_last_total_scheduledXX", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_21(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_LAST_TOTAL_SCHEDULED", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_22(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 1):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_23(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = None

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_24(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 2.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_25(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = None
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_26(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["XX_last_total_scheduledXX"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_27(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_LAST_TOTAL_SCHEDULED"] = info.get("total_scheduled", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_28(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get(None, 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_29(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", None)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_30(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get(0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_31(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", )
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_32(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("XXtotal_scheduledXX", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_33(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("TOTAL_SCHEDULED", 0)
        return scheduled

    # ------------------------------------------------------------------
    # 私有方法：目标计算
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_34(self, info: dict[str, Any]) -> float:
        """
        计算吞吐量目标：本步完成的任务数。

        当本步成功调度了一个任务（兼容分配且资源可用），
        吞吐量贡献为 +1。归一化到 [0, 1] 区间。

        Args:
            info: 原始 env.step() 返回的 info 字典

        Returns:
            float: 吞吐量目标值 [0, 1]
        """
        # 判断本步是否成功调度了任务
        # 通过检查 info 中的统计变化来判断
        scheduled = 0.0
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]

        # 检查本步是否有调度动作且兼容
        if env._current_task is not None or env._total_scheduled > 0:  # noqa: SIM102
            # 通过比较 mismatch_count 和 success 的变化来判断
            # 简化：如果本步 reward 包含执行奖励（非惩罚），则视为成功调度
            if info.get("total_scheduled", 0) > self._mo_stats.get("_last_total_scheduled", 0):
                scheduled = 1.0

        self._mo_stats["_last_total_scheduled"] = info.get("total_scheduled", 1)
        return scheduled

    @_mutmut_mutated(mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut)
    def _compute_balance(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_orig(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_1(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = None  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_2(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = None  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_3(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = None  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_4(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = None
        return float(np.clip(balance, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_5(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = +abs(quantum_util - classical_util)
        return float(np.clip(balance, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_6(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(None)
        return float(np.clip(balance, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_7(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util + classical_util)
        return float(np.clip(balance, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_8(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(None)

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_9(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(None, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_10(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, None, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_11(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, -1.0, None))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_12(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(-1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_13(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_14(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, -1.0, ))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_15(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, +1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_16(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, -2.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_17(self) -> float:
        """
        计算资源平衡目标：量子/经典资源利用率的平衡度。

        公式: balance = -|quantum_available_ratio - classical_load|
        完全平衡时为 0，越不平衡负值越大。

        Returns:
            float: 平衡度目标值 [-1, 0]
        """
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        quantum_util = env._quantum.available_ratio  # 量子可用比率（越高越空闲）
        classical_util = env._classical.load  # 经典负载（越高越忙）

        # 平衡度 = -|量子空闲率 - 经典负载率|
        # 当两者相等时最平衡，值为 0
        balance = -abs(quantum_util - classical_util)
        return float(np.clip(balance, -1.0, 1.0))

    @_mutmut_mutated(mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut)
    def _compute_quality(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_orig(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_1(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = None  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_2(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_3(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 1.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_4(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = None
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_5(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) * len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_6(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(None) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_7(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = None
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_8(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait * MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_9(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = +avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_10(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(None)

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_11(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(None, -1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_12(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, None, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_13(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, None))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_14(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(-1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_15(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_16(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, ))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_17(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, +1.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_18(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -2.0, 0.0))

    def xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_19(self) -> float:
        """
        计算服务质量目标：用户等待时间。

        公式: quality = -avg_wait / MAX_WAIT_STEPS
        等待时间越短，服务质量越好（值越接近 0）。

        Returns:
            float: 服务质量目标值 [-1, 0]
        """
        from src.scheduler.env import QuantumSchedulingEnv
        env: QuantumSchedulingEnv = self.env.unwrapped  # type: ignore[assignment]
        if not env._task_queue:
            return 0.0

        avg_wait = sum(t.wait_steps for t in env._task_queue) / len(env._task_queue)
        quality = -avg_wait / MAX_WAIT_STEPS
        return float(np.clip(quality, -1.0, 1.0))

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    @_mutmut_mutated(mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut)
    def _reset_mo_stats(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_orig(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_1(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "XXtotal_throughputXX": 0.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_2(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "TOTAL_THROUGHPUT": 0.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_3(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 1.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_4(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "XXtotal_balanceXX": 0.0,
            "total_quality": 0.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_5(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "TOTAL_BALANCE": 0.0,
            "total_quality": 0.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_6(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 1.0,
            "total_quality": 0.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_7(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "XXtotal_qualityXX": 0.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_8(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "TOTAL_QUALITY": 0.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_9(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "total_quality": 1.0,
            "steps": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_10(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "XXstepsXX": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_11(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "STEPS": 0,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_12(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "steps": 1,
            "_last_total_scheduled": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_13(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "steps": 0,
            "XX_last_total_scheduledXX": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_14(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "steps": 0,
            "_LAST_TOTAL_SCHEDULED": 0,
        }

    # ------------------------------------------------------------------
    # 私有方法：统计重置
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_15(self) -> dict[str, Any]:
        """
        重置多目标统计。

        Returns:
            dict: 初始化的统计字典
        """
        return {
            "total_throughput": 0.0,
            "total_balance": 0.0,
            "total_quality": 0.0,
            "steps": 0,
            "_last_total_scheduled": 1,
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    @_mutmut_mutated(mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut)
    def get_episode_objectives(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["total_throughput"],
            "balance": self._mo_stats["total_balance"],
            "quality": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_orig(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["total_throughput"],
            "balance": self._mo_stats["total_balance"],
            "quality": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_1(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "XXthroughputXX": self._mo_stats["total_throughput"],
            "balance": self._mo_stats["total_balance"],
            "quality": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_2(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "THROUGHPUT": self._mo_stats["total_throughput"],
            "balance": self._mo_stats["total_balance"],
            "quality": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_3(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["XXtotal_throughputXX"],
            "balance": self._mo_stats["total_balance"],
            "quality": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_4(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["TOTAL_THROUGHPUT"],
            "balance": self._mo_stats["total_balance"],
            "quality": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_5(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["total_throughput"],
            "XXbalanceXX": self._mo_stats["total_balance"],
            "quality": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_6(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["total_throughput"],
            "BALANCE": self._mo_stats["total_balance"],
            "quality": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_7(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["total_throughput"],
            "balance": self._mo_stats["XXtotal_balanceXX"],
            "quality": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_8(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["total_throughput"],
            "balance": self._mo_stats["TOTAL_BALANCE"],
            "quality": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_9(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["total_throughput"],
            "balance": self._mo_stats["total_balance"],
            "XXqualityXX": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_10(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["total_throughput"],
            "balance": self._mo_stats["total_balance"],
            "QUALITY": self._mo_stats["total_quality"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_11(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["total_throughput"],
            "balance": self._mo_stats["total_balance"],
            "quality": self._mo_stats["XXtotal_qualityXX"],
        }

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_12(self) -> dict[str, float]:
        """
        获取当前 episode 累积的多目标值。

        Returns:
            dict: {"throughput": ..., "balance": ..., "quality": ...}
        """
        return {
            "throughput": self._mo_stats["total_throughput"],
            "balance": self._mo_stats["total_balance"],
            "quality": self._mo_stats["TOTAL_QUALITY"],
        }

    @_mutmut_mutated(mutants_xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut)
    def set_weight_preset(self, preset: str) -> None:
        """
        通过预设名称切换权重。

        Args:
            preset: 预设名称，如 "throughput_heavy", "balance_heavy", "quality_heavy"
        """
        if preset not in DEFAULT_WEIGHTS:
            raise ValueError(f"未知权重预设 '{preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}")
        self._weights = list(DEFAULT_WEIGHTS[preset])

    def xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_orig(self, preset: str) -> None:
        """
        通过预设名称切换权重。

        Args:
            preset: 预设名称，如 "throughput_heavy", "balance_heavy", "quality_heavy"
        """
        if preset not in DEFAULT_WEIGHTS:
            raise ValueError(f"未知权重预设 '{preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}")
        self._weights = list(DEFAULT_WEIGHTS[preset])

    def xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_1(self, preset: str) -> None:
        """
        通过预设名称切换权重。

        Args:
            preset: 预设名称，如 "throughput_heavy", "balance_heavy", "quality_heavy"
        """
        if preset in DEFAULT_WEIGHTS:
            raise ValueError(f"未知权重预设 '{preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}")
        self._weights = list(DEFAULT_WEIGHTS[preset])

    def xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_2(self, preset: str) -> None:
        """
        通过预设名称切换权重。

        Args:
            preset: 预设名称，如 "throughput_heavy", "balance_heavy", "quality_heavy"
        """
        if preset not in DEFAULT_WEIGHTS:
            raise ValueError(None)
        self._weights = list(DEFAULT_WEIGHTS[preset])

    def xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_3(self, preset: str) -> None:
        """
        通过预设名称切换权重。

        Args:
            preset: 预设名称，如 "throughput_heavy", "balance_heavy", "quality_heavy"
        """
        if preset not in DEFAULT_WEIGHTS:
            raise ValueError(f"未知权重预设 '{preset}'，可选: {list(None)}")
        self._weights = list(DEFAULT_WEIGHTS[preset])

    def xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_4(self, preset: str) -> None:
        """
        通过预设名称切换权重。

        Args:
            preset: 预设名称，如 "throughput_heavy", "balance_heavy", "quality_heavy"
        """
        if preset not in DEFAULT_WEIGHTS:
            raise ValueError(f"未知权重预设 '{preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}")
        self._weights = None

    def xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_5(self, preset: str) -> None:
        """
        通过预设名称切换权重。

        Args:
            preset: 预设名称，如 "throughput_heavy", "balance_heavy", "quality_heavy"
        """
        if preset not in DEFAULT_WEIGHTS:
            raise ValueError(f"未知权重预设 '{preset}'，可选: {list(DEFAULT_WEIGHTS.keys())}")
        self._weights = list(None)

mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['_mutmut_orig'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_1'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_2'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_3'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_4'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_5'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_6'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_7'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_8'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_9'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_10'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_11'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_12'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_12 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_13'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_13 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_14'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_14 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_15'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_15 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_16'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_16 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_17'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_17 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_18'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_18 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_19'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_19 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_20'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_20 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_21'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_21 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_22'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_22 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_23'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_23 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ__init____mutmut['xǁMultiObjectiveRewardWrapperǁ__init____mutmut_24'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ__init____mutmut_24 # type: ignore # mutmut generated

mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['_mutmut_orig'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_1'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_2'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_3'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_4'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_5'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_6'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_7'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_8'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_9'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_10'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_11'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_12'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_13'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_14'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_15'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_16'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_17'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_18'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_18 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_19'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_19 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_20'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_20 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_21'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_21 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁreset__mutmut['xǁMultiObjectiveRewardWrapperǁreset__mutmut_22'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁreset__mutmut_22 # type: ignore # mutmut generated

mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['_mutmut_orig'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_1'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_2'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_3'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_4'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_5'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_6'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_7'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_8'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_9'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_10'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_11'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_12'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_13'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_14'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_15'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_16'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_17'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_18'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_18 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_19'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_19 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_20'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_20 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_21'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_21 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_22'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_22 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_23'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_23 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_24'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_24 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_25'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_25 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_26'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_26 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_27'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_27 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_28'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_28 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_29'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_29 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_30'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_30 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_31'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_31 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_32'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_32 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_33'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_33 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_34'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_34 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_35'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_35 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_36'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_36 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_37'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_37 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_38'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_38 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_39'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_39 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_40'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_40 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_41'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_41 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_42'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_42 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_43'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_43 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_44'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_44 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_45'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_45 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_46'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_46 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_47'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_47 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_48'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_48 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_49'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_49 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_50'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_50 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_51'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_51 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_52'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_52 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_53'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_53 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_54'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_54 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_55'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_55 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_56'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_56 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_57'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_57 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_58'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_58 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_59'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_59 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_60'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_60 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_61'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_61 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_62'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_62 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_63'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_63 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_64'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_64 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_65'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_65 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_66'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_66 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_67'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_67 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_68'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_68 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_69'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_69 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_70'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_70 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_71'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_71 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_72'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_72 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_73'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_73 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁstep__mutmut['xǁMultiObjectiveRewardWrapperǁstep__mutmut_74'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁstep__mutmut_74 # type: ignore # mutmut generated

mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['_mutmut_orig'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_1'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_2'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_3'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_4'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_5'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_6'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_7'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_8'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_9'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_10'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_11'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_12'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_13'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_14'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_15'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_16'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_17'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_18'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_18 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_19'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_19 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_20'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_20 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_21'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_21 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_22'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_22 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_23'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_23 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_24'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_24 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_25'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_25 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_26'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_26 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_27'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_27 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_28'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_28 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_29'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_29 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_30'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_30 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_31'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_31 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_32'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_32 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_33'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_33 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_34'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_throughput__mutmut_34 # type: ignore # mutmut generated

mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['_mutmut_orig'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_1'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_2'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_3'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_4'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_5'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_6'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_7'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_8'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_9'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_10'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_11'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_12'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_13'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_14'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_15'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_16'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_17'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_balance__mutmut_17 # type: ignore # mutmut generated

mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['_mutmut_orig'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_1'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_2'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_3'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_4'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_5'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_6'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_7'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_8'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_9'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_10'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_11'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_12'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_13'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_14'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_15'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_16'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_17'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_18'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_18 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut['xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_19'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_compute_quality__mutmut_19 # type: ignore # mutmut generated

mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['_mutmut_orig'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_1'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_2'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_3'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_4'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_5'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_6'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_7'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_8'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_9'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_10'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_11'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_12'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_13'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_14'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut['xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_15'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁ_reset_mo_stats__mutmut_15 # type: ignore # mutmut generated

mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['_mutmut_orig'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_1'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_2'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_3'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_4'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_5'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_6'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_7'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_8'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_9'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_10'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_11'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut['xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_12'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁget_episode_objectives__mutmut_12 # type: ignore # mutmut generated

mutants_xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut['_mutmut_orig'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut['xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_1'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut['xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_2'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut['xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_3'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut['xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_4'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut['xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_5'] = MultiObjectiveRewardWrapper.xǁMultiObjectiveRewardWrapperǁset_weight_preset__mutmut_5 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut: MutantDict = {}  # type: ignore


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


@_mutmut_mutated(mutants_x_make_mo_env__mutmut)
def make_mo_env(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_orig(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_1(
    max_qubits: int = 21,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_2(
    max_qubits: int = 20,
    max_steps: int = 201,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_3(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = None
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_4(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=None,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_5(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=None,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_6(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=None,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_7(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=None,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_8(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_9(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_10(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_11(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_12(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(None, weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_13(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=None, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_14(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, weight_preset=None)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_15(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(weights=weights, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_16(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weight_preset=weight_preset)


# ---------------------------------------------------------------------------
# 工厂函数
# ---------------------------------------------------------------------------


def x_make_mo_env__mutmut_17(
    max_qubits: int = 20,
    max_steps: int = 200,
    weights: list[float] | None = None,
    weight_preset: str | None = None,
    seed: int | None = None,
    machine_configs: Any | None = None,
) -> MultiObjectiveRewardWrapper:
    """
    创建多目标调度环境的便捷工厂函数。

    Args:
        max_qubits: 最大量子比特数
        max_steps: 最大步数
        weights: 3 元素权重列表
        weight_preset: 预定义权重名称
        seed: 随机种子
        machine_configs: 多机器配置（可选）

    Returns:
        MultiObjectiveRewardWrapper: 包装好的多目标环境
    """
    env = QuantumSchedulingEnv(
        max_qubits=max_qubits,
        max_steps=max_steps,
        seed=seed,
        machine_configs=machine_configs,
    )
    return MultiObjectiveRewardWrapper(env, weights=weights, )

mutants_x_make_mo_env__mutmut['_mutmut_orig'] = x_make_mo_env__mutmut_orig # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_1'] = x_make_mo_env__mutmut_1 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_2'] = x_make_mo_env__mutmut_2 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_3'] = x_make_mo_env__mutmut_3 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_4'] = x_make_mo_env__mutmut_4 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_5'] = x_make_mo_env__mutmut_5 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_6'] = x_make_mo_env__mutmut_6 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_7'] = x_make_mo_env__mutmut_7 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_8'] = x_make_mo_env__mutmut_8 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_9'] = x_make_mo_env__mutmut_9 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_10'] = x_make_mo_env__mutmut_10 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_11'] = x_make_mo_env__mutmut_11 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_12'] = x_make_mo_env__mutmut_12 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_13'] = x_make_mo_env__mutmut_13 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_14'] = x_make_mo_env__mutmut_14 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_15'] = x_make_mo_env__mutmut_15 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_16'] = x_make_mo_env__mutmut_16 # type: ignore # mutmut generated
mutants_x_make_mo_env__mutmut['x_make_mo_env__mutmut_17'] = x_make_mo_env__mutmut_17 # type: ignore # mutmut generated
