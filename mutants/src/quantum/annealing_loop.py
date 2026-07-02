"""
量子退火异步闭环训练模块

实现 "RL 训练 → 周期性触发退火优化 → 反馈权重 → 继续训练" 的全自动异步流程：
    - 训练线程通过 queue.Queue 提交退火任务，不被退火求解阻塞
    - 工作线程在后台完成 QUBO 退火、验证集评估、效果追踪
    - 优化后的权重在下一个 RL rollout 开始前回写到训练模型
    - 根据退火效果自适应调整触发频率
    - 真机退火失败时自动重试并降级为模拟退火
"""

import copy
import json
import logging
import os
import queue
import threading
import time
import types
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁstart__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁget_pending_result__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁget_history__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut: MutantDict = {}  # type: ignore


class AsyncAnnealingLoop:
    """
    异步量子退火闭环控制器

    以生产者-消费者模式运行：
        - 生产者：RL 训练回调（AsyncAnnealingCallback）在训练步达到触发条件时，
          将当前模型引用提交到任务队列
        - 消费者：独立工作线程从队列取出任务，复制策略网络进行退火优化，
          并在验证环境上比较退火前后的平均奖励，最后将优化权重暂存到 pending_result

    Attributes:
        optimizer          : 量子退火优化器（需实现 optimize_policy 方法）
        validation_env     : 用于评估退火效果的 Gymnasium 环境
        eval_episodes      : 每次评估的回合数
        eval_deterministic : 评估时是否使用确定性策略
        initial_interval   : 初始退火触发间隔（步数）
        min_interval       : 最小触发间隔
        max_interval       : 最大触发间隔
        improvement_threshold: 判断退火有效的奖励提升阈值
        retry_delays       : 真机失败后的重试等待时间（秒）
        log_path           : 退火效果日志保存路径（JSON）
    """

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁ__init____mutmut)
    def __init__(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_orig(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_1(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 4,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_2(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = False,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_3(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5001,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_4(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1001,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_5(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20001,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_6(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 1.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_7(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "XXresults/annealing_loop_log.jsonXX",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_8(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "RESULTS/ANNEALING_LOOP_LOG.JSON",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_9(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 2,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_10(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = None
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_11(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = None
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_12(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = None
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_13(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(None)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_14(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = None
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_15(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(None)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_16(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = None
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_17(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(None)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_18(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = None
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_19(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(None)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_20(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = None
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_21(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(None)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_22(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = None
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_23(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_24(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [6.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_25(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 16.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_26(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = None

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_27(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(None)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_28(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = None
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_29(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(None)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_30(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = None
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_31(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 1
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_32(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = None

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_33(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 1

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_34(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = None
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_35(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=None)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_36(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = ""
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_37(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_38(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = None
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_39(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = None
        self._thread: threading.Thread | None = None

    def xǁAsyncAnnealingLoopǁ__init____mutmut_40(
        self,
        optimizer: Any,
        validation_env: Any,
        eval_episodes: int = 3,
        eval_deterministic: bool = True,
        initial_interval: int = 5000,
        min_interval: int = 1000,
        max_interval: int = 20000,
        improvement_threshold: float = 0.0,
        retry_delays: list[float] | None = None,
        log_path: str = "results/annealing_loop_log.json",
        queue_maxsize: int = 1,
    ):
        """
        初始化异步退火闭环

        Args:
            optimizer           : 量子退火优化器实例
            validation_env      : 验证环境，用于计算退火前后的奖励变化
            eval_episodes       : 每次评估运行几个回合，默认 3
            eval_deterministic  : 评估是否使用确定性策略，默认 True
            initial_interval    : 初始退火触发间隔，默认 5000 步
            min_interval        : 最小触发间隔，默认 1000 步
            max_interval        : 最大触发间隔，默认 20000 步
            improvement_threshold: 奖励提升阈值，默认 0.0
            retry_delays        : 真机失败重试等待时间列表，默认 [5.0, 15.0]
            log_path            : 效果日志保存路径
            queue_maxsize       : 任务队列最大长度，默认 1（避免堆积）
        """
        self.optimizer = optimizer
        self.validation_env = validation_env
        self.eval_episodes = int(eval_episodes)
        self.eval_deterministic = bool(eval_deterministic)
        self.min_interval = int(min_interval)
        self.max_interval = int(max_interval)
        self.improvement_threshold = float(improvement_threshold)
        self.retry_delays = retry_delays if retry_delays is not None else [5.0, 15.0]
        self.log_path = str(log_path)

        self._current_interval = int(initial_interval)
        self._consecutive_good = 0
        self._consecutive_bad = 0

        self._queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=queue_maxsize)
        self._pending_result: dict[str, Any] | None = None
        self._history: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = ""

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁstart__mutmut)
    def start(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_orig(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_1(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None or self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_2(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_3(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning(None)
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_4(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("XX异步退火工作线程已启动，跳过重复启动XX")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_5(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = None
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_6(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=None, daemon=True)
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_7(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, daemon=None)
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_8(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(daemon=True)
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_9(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, )
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_10(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, daemon=False)
        self._thread.start()
        logger.info("异步退火工作线程已启动")

    def xǁAsyncAnnealingLoopǁstart__mutmut_11(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()
        logger.info(None)

    def xǁAsyncAnnealingLoopǁstart__mutmut_12(self) -> None:
        """启动异步退火工作线程。"""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("异步退火工作线程已启动，跳过重复启动")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()
        logger.info("XX异步退火工作线程已启动XX")

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut)
    def shutdown(self, wait: bool = True, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("异步退火工作线程未能在超时时间内结束")
        logger.info("异步退火工作线程已关闭")

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_orig(self, wait: bool = True, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("异步退火工作线程未能在超时时间内结束")
        logger.info("异步退火工作线程已关闭")

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_1(self, wait: bool = False, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("异步退火工作线程未能在超时时间内结束")
        logger.info("异步退火工作线程已关闭")

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_2(self, wait: bool = True, timeout: float | None = 301.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("异步退火工作线程未能在超时时间内结束")
        logger.info("异步退火工作线程已关闭")

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_3(self, wait: bool = True, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is not None or self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("异步退火工作线程未能在超时时间内结束")
        logger.info("异步退火工作线程已关闭")

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_4(self, wait: bool = True, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait or self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("异步退火工作线程未能在超时时间内结束")
        logger.info("异步退火工作线程已关闭")

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_5(self, wait: bool = True, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("异步退火工作线程未能在超时时间内结束")
        logger.info("异步退火工作线程已关闭")

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_6(self, wait: bool = True, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=None)
            if self._thread.is_alive():
                logger.warning("异步退火工作线程未能在超时时间内结束")
        logger.info("异步退火工作线程已关闭")

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_7(self, wait: bool = True, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning(None)
        logger.info("异步退火工作线程已关闭")

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_8(self, wait: bool = True, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("XX异步退火工作线程未能在超时时间内结束XX")
        logger.info("异步退火工作线程已关闭")

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_9(self, wait: bool = True, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("异步退火工作线程未能在超时时间内结束")
        logger.info(None)

    def xǁAsyncAnnealingLoopǁshutdown__mutmut_10(self, wait: bool = True, timeout: float | None = 300.0) -> None:
        """
        关闭异步退火工作线程

        Args:
            wait   : 是否等待工作线程结束，默认 True
            timeout: 等待超时时间（秒），默认 300 秒（覆盖一次完整退火优化）
        """
        self._stop_event.set()
        if wait and self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("异步退火工作线程未能在超时时间内结束")
        logger.info("XX异步退火工作线程已关闭XX")

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut)
    def submit(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"policy": policy, "step": int(step)})
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return True
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_orig(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"policy": policy, "step": int(step)})
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return True
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_1(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait(None)
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return True
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_2(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"XXpolicyXX": policy, "step": int(step)})
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return True
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_3(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"POLICY": policy, "step": int(step)})
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return True
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_4(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"policy": policy, "XXstepXX": int(step)})
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return True
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_5(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"policy": policy, "STEP": int(step)})
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return True
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_6(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"policy": policy, "step": int(None)})
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return True
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_7(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"policy": policy, "step": int(step)})
            logger.info(None)
            return True
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_8(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"policy": policy, "step": int(step)})
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return False
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_9(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"policy": policy, "step": int(step)})
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return True
        except queue.Full:
            logger.warning(None)
            return False

    def xǁAsyncAnnealingLoopǁsubmit__mutmut_10(self, policy: Any, step: int) -> bool:
        """
        向退火任务队列提交一个优化请求

        该方法只把策略网络快照放入队列，不做退火计算，因此不会阻塞 RL 训练。
        调用方应确保传入的 policy 是训练模型权重的独立副本（深拷贝），
        避免工作线程与训练线程竞争同一组参数。

        Args:
            policy: 策略网络快照（需实现 predict / state_dict / load_state_dict）
            step  : 当前训练步数

        Returns:
            是否成功提交；队列满时返回 False
        """
        try:
            self._queue.put_nowait({"policy": policy, "step": int(step)})
            logger.info(f"[退火闭环] 步数 {step}: 已提交退火任务到异步队列")
            return True
        except queue.Full:
            logger.warning(f"[退火闭环] 步数 {step}: 退火任务队列已满，跳过本次提交")
            return True

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁget_pending_result__mutmut)
    def get_pending_result(self) -> dict[str, Any] | None:
        """获取并清空当前待回写的优化结果（非线程安全调用需自行保证在主线程）。"""
        with self._lock:
            result = self._pending_result
            self._pending_result = None
            return result

    def xǁAsyncAnnealingLoopǁget_pending_result__mutmut_orig(self) -> dict[str, Any] | None:
        """获取并清空当前待回写的优化结果（非线程安全调用需自行保证在主线程）。"""
        with self._lock:
            result = self._pending_result
            self._pending_result = None
            return result

    def xǁAsyncAnnealingLoopǁget_pending_result__mutmut_1(self) -> dict[str, Any] | None:
        """获取并清空当前待回写的优化结果（非线程安全调用需自行保证在主线程）。"""
        with self._lock:
            result = None
            self._pending_result = None
            return result

    def xǁAsyncAnnealingLoopǁget_pending_result__mutmut_2(self) -> dict[str, Any] | None:
        """获取并清空当前待回写的优化结果（非线程安全调用需自行保证在主线程）。"""
        with self._lock:
            result = self._pending_result
            self._pending_result = ""
            return result

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut)
    def peek_pending_result(self) -> dict[str, Any] | None:
        """查看当前待回写的优化结果，但不清空。"""
        with self._lock:
            return copy.deepcopy(self._pending_result) if self._pending_result is not None else None

    def xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_orig(self) -> dict[str, Any] | None:
        """查看当前待回写的优化结果，但不清空。"""
        with self._lock:
            return copy.deepcopy(self._pending_result) if self._pending_result is not None else None

    def xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_1(self) -> dict[str, Any] | None:
        """查看当前待回写的优化结果，但不清空。"""
        with self._lock:
            return copy.deepcopy(None) if self._pending_result is not None else None

    def xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_2(self) -> dict[str, Any] | None:
        """查看当前待回写的优化结果，但不清空。"""
        with self._lock:
            return copy.copy(self._pending_result) if self._pending_result is not None else None

    def xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_3(self) -> dict[str, Any] | None:
        """查看当前待回写的优化结果，但不清空。"""
        with self._lock:
            return copy.deepcopy(self._pending_result) if self._pending_result is None else None

    def get_current_interval(self) -> int:
        """获取当前自适应退火触发间隔。"""
        with self._lock:
            return self._current_interval

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁget_history__mutmut)
    def get_history(self) -> list[dict[str, Any]]:
        """获取退火效果历史记录（深拷贝，避免外部修改）。"""
        with self._lock:
            return copy.deepcopy(self._history)

    def xǁAsyncAnnealingLoopǁget_history__mutmut_orig(self) -> list[dict[str, Any]]:
        """获取退火效果历史记录（深拷贝，避免外部修改）。"""
        with self._lock:
            return copy.deepcopy(self._history)

    def xǁAsyncAnnealingLoopǁget_history__mutmut_1(self) -> list[dict[str, Any]]:
        """获取退火效果历史记录（深拷贝，避免外部修改）。"""
        with self._lock:
            return copy.deepcopy(None)

    def xǁAsyncAnnealingLoopǁget_history__mutmut_2(self) -> list[dict[str, Any]]:
        """获取退火效果历史记录（深拷贝，避免外部修改）。"""
        with self._lock:
            return copy.copy(self._history)

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut)
    def _worker_loop(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_orig(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_1(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() and not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_2(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_3(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_4(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = None
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_5(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=None)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_6(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=1.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_7(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                break

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_8(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = None
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_9(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["XXpolicyXX"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_10(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["POLICY"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_11(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = None

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_12(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["XXstepXX"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_13(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["STEP"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_14(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = None
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_15(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(None)
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_16(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(None).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_17(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                break

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_18(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = None

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_19(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=None)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_20(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = None
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_21(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(None)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_22(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = None
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_23(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(None, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_24(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, None)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_25(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_26(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, )
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_27(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = None
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_28(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(None)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_29(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(None)
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_30(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(None).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_31(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                break

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_32(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = None
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_33(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward + old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_34(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(None)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_35(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = None

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_36(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "XXstepXX": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_37(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "STEP": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_38(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "XXtimestampXX": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_39(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "TIMESTAMP": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_40(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "XXold_rewardXX": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_41(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "OLD_REWARD": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_42(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "XXnew_rewardXX": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_43(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "NEW_REWARD": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_44(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "XXdeltaXX": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_45(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "DELTA": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_46(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "XXintervalXX": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_47(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "INTERVAL": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_48(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = None
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_49(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "XXstepXX": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_50(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "STEP": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_51(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "XXstate_dictXX": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_52(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "STATE_DICT": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_53(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(None),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_54(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.copy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_55(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "XXdeltaXX": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_56(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "DELTA": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_57(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "XXtimestampXX": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_58(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "TIMESTAMP": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_59(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["XXtimestampXX"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_60(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["TIMESTAMP"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_61(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(None)

            self._save_log()

            logger.info(
                f"[退火闭环] 步数 {step}: 旧奖励={old_reward:.4f}, "
                f"新奖励={new_reward:.4f}, delta={delta:.4f}, "
                f"当前间隔={self.get_current_interval()}"
            )

    def xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_62(self) -> None:
        """退火工作线程主循环：消费队列任务并完成优化、评估、记录。"""
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                task = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            eval_policy = task["policy"]
            step = task["step"]

            try:
                # 确保策略网络在 CPU 评估模式，避免影响训练设备上的张量
                eval_policy = eval_policy.cpu().eval()
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 准备策略网络失败 ({type(e).__name__}: {e})")
                continue

            agent_wrapper = types.SimpleNamespace(policy=eval_policy)

            try:
                old_reward = self._evaluate_policy(eval_policy)
                optimized_wrapper = self._run_annealing_with_retries(agent_wrapper, step)
                new_reward = self._evaluate_policy(optimized_wrapper.policy)
            except Exception as e:
                logger.error(f"[退火闭环] 步数 {step}: 退火或评估失败 ({type(e).__name__}: {e})")
                continue

            delta = new_reward - old_reward
            self._update_interval(delta)

            record = {
                "step": step,
                "timestamp": time.time(),
                "old_reward": old_reward,
                "new_reward": new_reward,
                "delta": delta,
                "interval": self.get_current_interval(),
            }

            with self._lock:
                self._pending_result = {
                    "step": step,
                    "state_dict": copy.deepcopy(optimized_wrapper.policy.state_dict()),
                    "delta": delta,
                    "timestamp": record["timestamp"],
                }
                self._history.append(record)

            self._save_log()

            logger.info(
                None
            )

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut)
    def _run_annealing_with_retries(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_orig(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_1(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(None):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_2(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(None, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_3(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=None)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_4(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_5(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, )
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_6(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=False)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_7(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(None, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_8(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, None, True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_9(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", None):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_10(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr("simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_11(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_12(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", ):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_13(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "XXsimulation_modeXX", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_14(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "SIMULATION_MODE", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_15(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", False):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_16(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    None
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_17(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt - 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_18(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 2} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_19(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(None).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_20(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(None)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_21(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(None)
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_22(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = None
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_23(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = False
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_24(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(None, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_25(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=None)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_26(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_27(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, )
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_28(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=False)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(e).__name__}: {e})")
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_29(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(None)
            raise

    def xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_30(self, agent_wrapper: Any, step: int) -> Any:
        """
        执行退火优化，并处理真机失败重试与降级

        重试策略：
            - 第一次在真机模式下失败，等待 retry_delays[0] 秒后重试
            - 第二次失败，等待 retry_delays[1] 秒后重试
            - 第三次失败，将优化器切换到仿真模式并最后尝试一次
            - 若仍失败，则抛出异常由工作线程记录

        Args:
            agent_wrapper: 包装了待优化策略网络的简单对象
            step         : 当前训练步数，仅用于日志

        Returns:
            优化后的 agent_wrapper
        """
        for attempt, delay in enumerate(self.retry_delays):
            try:
                return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
            except Exception as e:
                if getattr(self.optimizer, "simulation_mode", True):
                    raise
                logger.warning(
                    f"[退火闭环] 步数 {step}: 真机退火失败（第 {attempt + 1} 次），"
                    f"{delay}s 后重试 ({type(e).__name__}: {e})"
                )
                time.sleep(delay)

        # 重试次数耗尽，降级为仿真退火
        try:
            logger.warning(f"[退火闭环] 步数 {step}: 真机退火重试耗尽，降级为仿真退火")
            self.optimizer.simulation_mode = True
            return self.optimizer.optimize_policy(agent_wrapper, head_only=True)
        except Exception as e:
            logger.error(f"[退火闭环] 步数 {step}: 仿真退火也失败 ({type(None).__name__}: {e})")
            raise

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut)
    def _evaluate_policy(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_orig(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_1(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = None
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_2(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(None):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_3(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = None
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_4(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = None
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_5(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = None

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_6(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = None
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_7(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = True
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_8(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = None
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_9(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 1.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_10(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_11(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = None
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_12(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(None, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_13(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=None)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_14(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_15(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, )
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_16(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = None
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_17(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(None)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_18(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = None
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_19(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward = float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_20(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward -= float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_21(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(None)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_22(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = None
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_23(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(None)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_24(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated and truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_25(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(None)

        return float(np.mean(episode_rewards))

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_26(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(None)

    def xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_27(self, policy: Any) -> float:
        """
        在验证环境上评估策略网络的平均回合奖励

        Args:
            policy: 策略网络（需实现 predict 方法）

        Returns:
            平均回合奖励
        """
        episode_rewards: list[float] = []
        for _ in range(self.eval_episodes):
            reset_output = self.validation_env.reset()
            if isinstance(reset_output, tuple):
                obs, _info = reset_output
            else:
                obs = reset_output

            done = False
            total_reward = 0.0
            while not done:
                action, _ = policy.predict(obs, deterministic=self.eval_deterministic)
                step_output = self.validation_env.step(action)
                obs, reward, terminated, truncated, _info = step_output
                total_reward += float(reward)
                done = bool(terminated or truncated)
            episode_rewards.append(total_reward)

        return float(np.mean(None))

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut)
    def _update_interval(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_orig(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_1(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta >= self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_2(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good = 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_3(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good -= 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_4(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 2
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_5(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = None
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_6(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 1
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_7(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good > 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_8(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 4:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_9(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = None
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_10(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(None, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_11(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, None)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_12(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_13(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, )
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_14(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval / 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_15(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 3)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_16(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = None
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_17(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 1
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_18(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        None
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_19(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta <= self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_20(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad = 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_21(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad -= 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_22(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 2
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_23(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = None
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_24(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 1
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_25(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad > 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_26(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 4:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_27(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = None
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_28(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(None, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_29(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, None)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_30(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_31(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, )
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_32(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval / 2)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_33(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 3)
                    self._consecutive_bad = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_34(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = None
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_35(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 1
                    logger.info(
                        f"[退火闭环] 连续 3 次无效，触发间隔延长为 {self._current_interval}"
                    )

    def xǁAsyncAnnealingLoopǁ_update_interval__mutmut_36(self, delta: float) -> None:
        """
        根据退火效果自适应调整触发间隔

        规则：
            - 连续 3 次 delta > threshold：触发间隔减半（不低于 min_interval）
            - 连续 3 次 delta < threshold：触发间隔加倍（不高于 max_interval）

        Args:
            delta: 退火后奖励 - 退火前奖励
        """
        with self._lock:
            if delta > self.improvement_threshold:
                self._consecutive_good += 1
                self._consecutive_bad = 0
                if self._consecutive_good >= 3:
                    self._current_interval = max(self.min_interval, self._current_interval // 2)
                    self._consecutive_good = 0
                    logger.info(
                        f"[退火闭环] 连续 3 次有效，触发间隔缩短为 {self._current_interval}"
                    )
            elif delta < self.improvement_threshold:
                self._consecutive_bad += 1
                self._consecutive_good = 0
                if self._consecutive_bad >= 3:
                    self._current_interval = min(self.max_interval, self._current_interval * 2)
                    self._consecutive_bad = 0
                    logger.info(
                        None
                    )

    @_mutmut_mutated(mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut)
    def _save_log(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_orig(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_1(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = None
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_2(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(None)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_3(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(None, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_4(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=None)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_5(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_6(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, )
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_7(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=False)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_8(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = None
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_9(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(None)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_10(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.copy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_11(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(None, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_12(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, None, encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_13(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding=None) as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_14(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open("w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_15(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_16(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", ) as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_17(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "XXwXX", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_18(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "W", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_19(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="XXutf-8XX") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_20(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="UTF-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_21(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(None, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_22(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, None, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_23(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=None, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_24(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=None)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_25(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_26(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_27(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_28(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, )
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_29(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=True, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_30(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=3)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(e).__name__}: {e})")

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_31(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(None)

    def xǁAsyncAnnealingLoopǁ_save_log__mutmut_32(self) -> None:
        """将退火效果历史保存为 JSON 日志。"""
        try:
            log_dir = os.path.dirname(self.log_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            with self._lock:
                history = copy.deepcopy(self._history)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[退火闭环] 保存日志失败 ({type(None).__name__}: {e})")

mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_3'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_4'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_5'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_6'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_7'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_8'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_9'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_10'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_10 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_11'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_11 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_12'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_12 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_13'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_13 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_14'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_14 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_15'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_15 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_16'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_16 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_17'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_17 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_18'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_18 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_19'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_19 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_20'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_20 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_21'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_21 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_22'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_22 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_23'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_23 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_24'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_24 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_25'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_25 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_26'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_26 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_27'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_27 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_28'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_28 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_29'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_29 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_30'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_30 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_31'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_31 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_32'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_32 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_33'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_33 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_34'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_34 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_35'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_35 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_36'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_36 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_37'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_37 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_38'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_38 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_39'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_39 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ__init____mutmut['xǁAsyncAnnealingLoopǁ__init____mutmut_40'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ__init____mutmut_40 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁstart__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_3'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_4'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_5'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_6'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_7'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_8'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_9'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_10'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_11'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁstart__mutmut['xǁAsyncAnnealingLoopǁstart__mutmut_12'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁstart__mutmut_12 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['xǁAsyncAnnealingLoopǁshutdown__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['xǁAsyncAnnealingLoopǁshutdown__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['xǁAsyncAnnealingLoopǁshutdown__mutmut_3'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['xǁAsyncAnnealingLoopǁshutdown__mutmut_4'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['xǁAsyncAnnealingLoopǁshutdown__mutmut_5'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['xǁAsyncAnnealingLoopǁshutdown__mutmut_6'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['xǁAsyncAnnealingLoopǁshutdown__mutmut_7'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['xǁAsyncAnnealingLoopǁshutdown__mutmut_8'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['xǁAsyncAnnealingLoopǁshutdown__mutmut_9'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁshutdown__mutmut['xǁAsyncAnnealingLoopǁshutdown__mutmut_10'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁshutdown__mutmut_10 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['xǁAsyncAnnealingLoopǁsubmit__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['xǁAsyncAnnealingLoopǁsubmit__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['xǁAsyncAnnealingLoopǁsubmit__mutmut_3'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['xǁAsyncAnnealingLoopǁsubmit__mutmut_4'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['xǁAsyncAnnealingLoopǁsubmit__mutmut_5'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['xǁAsyncAnnealingLoopǁsubmit__mutmut_6'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['xǁAsyncAnnealingLoopǁsubmit__mutmut_7'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['xǁAsyncAnnealingLoopǁsubmit__mutmut_8'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['xǁAsyncAnnealingLoopǁsubmit__mutmut_9'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁsubmit__mutmut['xǁAsyncAnnealingLoopǁsubmit__mutmut_10'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁsubmit__mutmut_10 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁget_pending_result__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁget_pending_result__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁget_pending_result__mutmut['xǁAsyncAnnealingLoopǁget_pending_result__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁget_pending_result__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁget_pending_result__mutmut['xǁAsyncAnnealingLoopǁget_pending_result__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁget_pending_result__mutmut_2 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut['xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut['xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut['xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_3'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁpeek_pending_result__mutmut_3 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁget_history__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁget_history__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁget_history__mutmut['xǁAsyncAnnealingLoopǁget_history__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁget_history__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁget_history__mutmut['xǁAsyncAnnealingLoopǁget_history__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁget_history__mutmut_2 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_3'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_4'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_5'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_6'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_7'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_8'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_9'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_10'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_11'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_12'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_13'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_14'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_15'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_16'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_17'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_17 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_18'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_18 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_19'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_19 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_20'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_20 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_21'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_21 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_22'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_22 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_23'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_23 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_24'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_24 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_25'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_25 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_26'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_26 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_27'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_27 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_28'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_28 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_29'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_29 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_30'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_30 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_31'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_31 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_32'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_32 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_33'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_33 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_34'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_34 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_35'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_35 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_36'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_36 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_37'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_37 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_38'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_38 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_39'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_39 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_40'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_40 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_41'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_41 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_42'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_42 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_43'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_43 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_44'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_44 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_45'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_45 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_46'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_46 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_47'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_47 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_48'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_48 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_49'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_49 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_50'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_50 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_51'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_51 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_52'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_52 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_53'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_53 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_54'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_54 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_55'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_55 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_56'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_56 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_57'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_57 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_58'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_58 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_59'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_59 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_60'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_60 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_61'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_61 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_worker_loop__mutmut['xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_62'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_worker_loop__mutmut_62 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_3'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_4'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_5'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_6'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_7'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_8'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_9'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_10'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_11'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_12'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_13'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_14'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_15'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_16'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_17'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_17 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_18'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_18 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_19'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_19 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_20'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_20 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_21'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_21 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_22'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_22 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_23'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_23 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_24'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_24 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_25'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_25 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_26'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_26 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_27'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_27 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_28'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_28 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_29'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_29 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut['xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_30'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_run_annealing_with_retries__mutmut_30 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_3'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_4'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_5'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_6'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_7'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_8'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_9'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_10'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_11'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_12'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_13'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_14'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_15'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_16'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_17'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_17 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_18'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_18 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_19'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_19 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_20'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_20 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_21'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_21 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_22'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_22 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_23'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_23 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_24'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_24 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_25'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_25 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_26'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_26 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut['xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_27'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_evaluate_policy__mutmut_27 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_3'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_4'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_5'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_6'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_7'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_8'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_9'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_10'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_11'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_12'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_13'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_14'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_15'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_16'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_17'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_17 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_18'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_18 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_19'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_19 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_20'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_20 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_21'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_21 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_22'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_22 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_23'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_23 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_24'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_24 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_25'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_25 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_26'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_26 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_27'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_27 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_28'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_28 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_29'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_29 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_30'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_30 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_31'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_31 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_32'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_32 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_33'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_33 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_34'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_34 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_35'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_35 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_update_interval__mutmut['xǁAsyncAnnealingLoopǁ_update_interval__mutmut_36'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_update_interval__mutmut_36 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['_mutmut_orig'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_1'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_2'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_3'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_4'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_5'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_6'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_7'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_8'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_9'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_10'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_11'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_12'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_13'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_14'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_15'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_16'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_17'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_17 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_18'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_18 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_19'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_19 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_20'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_20 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_21'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_21 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_22'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_22 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_23'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_23 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_24'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_24 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_25'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_25 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_26'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_26 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_27'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_27 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_28'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_28 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_29'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_29 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_30'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_30 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_31'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_31 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingLoopǁ_save_log__mutmut['xǁAsyncAnnealingLoopǁ_save_log__mutmut_32'] = AsyncAnnealingLoop.xǁAsyncAnnealingLoopǁ_save_log__mutmut_32 # type: ignore # mutmut generated


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print("AsyncAnnealingLoop 模块已加载，请通过 train_with_annealing_loop.py 使用")
