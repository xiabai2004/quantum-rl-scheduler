"""
异步量子退火训练回调

替代原有的同步 AnnealingCallback，将退火优化放到独立工作线程中执行，
使 RL 训练不被退火求解阻塞，并在每个 rollout 开始前将优化后的权重回写到模型。
"""

import copy
import logging

from stable_baselines3.common.callbacks import BaseCallback

from src.quantum.annealing_loop import AsyncAnnealingLoop

logger = logging.getLogger(__name__)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁAsyncAnnealingCallbackǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingCallbackǁ_init_callback__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut: MutantDict = {}  # type: ignore


class AsyncAnnealingCallback(BaseCallback):
    """
    异步量子退火触发与权重回写回调

    工作流程：
        1. _on_step: 每步检查是否达到自适应触发间隔，达到则向 AsyncAnnealingLoop
           提交一个退火任务（仅放入队列，不阻塞训练）
        2. _on_rollout_start: 在每个 rollout 收集数据前，检查是否有已完成并暂存的
           优化权重，若有则通过 model.policy.load_state_dict 回写
        3. _on_training_end: 关闭异步退火工作线程

    Attributes:
        loop          : 异步退火闭环控制器
        verbose       : 日志详细程度
    """

    @_mutmut_mutated(mutants_xǁAsyncAnnealingCallbackǁ__init____mutmut)
    def __init__(
        self,
        loop: AsyncAnnealingLoop,
        verbose: int = 0,
    ):
        """
        初始化异步退火回调

        Args:
            loop   : AsyncAnnealingLoop 实例
            verbose: 日志详细程度，0=静默，1=打印关键事件
        """
        super().__init__(verbose)
        self.loop = loop
        self._next_trigger_step: int | None = None

    def xǁAsyncAnnealingCallbackǁ__init____mutmut_orig(
        self,
        loop: AsyncAnnealingLoop,
        verbose: int = 0,
    ):
        """
        初始化异步退火回调

        Args:
            loop   : AsyncAnnealingLoop 实例
            verbose: 日志详细程度，0=静默，1=打印关键事件
        """
        super().__init__(verbose)
        self.loop = loop
        self._next_trigger_step: int | None = None

    def xǁAsyncAnnealingCallbackǁ__init____mutmut_1(
        self,
        loop: AsyncAnnealingLoop,
        verbose: int = 1,
    ):
        """
        初始化异步退火回调

        Args:
            loop   : AsyncAnnealingLoop 实例
            verbose: 日志详细程度，0=静默，1=打印关键事件
        """
        super().__init__(verbose)
        self.loop = loop
        self._next_trigger_step: int | None = None

    def xǁAsyncAnnealingCallbackǁ__init____mutmut_2(
        self,
        loop: AsyncAnnealingLoop,
        verbose: int = 0,
    ):
        """
        初始化异步退火回调

        Args:
            loop   : AsyncAnnealingLoop 实例
            verbose: 日志详细程度，0=静默，1=打印关键事件
        """
        super().__init__(None)
        self.loop = loop
        self._next_trigger_step: int | None = None

    def xǁAsyncAnnealingCallbackǁ__init____mutmut_3(
        self,
        loop: AsyncAnnealingLoop,
        verbose: int = 0,
    ):
        """
        初始化异步退火回调

        Args:
            loop   : AsyncAnnealingLoop 实例
            verbose: 日志详细程度，0=静默，1=打印关键事件
        """
        super().__init__(verbose)
        self.loop = None
        self._next_trigger_step: int | None = None

    def xǁAsyncAnnealingCallbackǁ__init____mutmut_4(
        self,
        loop: AsyncAnnealingLoop,
        verbose: int = 0,
    ):
        """
        初始化异步退火回调

        Args:
            loop   : AsyncAnnealingLoop 实例
            verbose: 日志详细程度，0=静默，1=打印关键事件
        """
        super().__init__(verbose)
        self.loop = loop
        self._next_trigger_step: int | None = ""

    @_mutmut_mutated(mutants_xǁAsyncAnnealingCallbackǁ_init_callback__mutmut)
    def _init_callback(self) -> None:
        """回调初始化：启动异步退火工作线程并设置首次触发步数。"""
        self.loop.start()
        self._next_trigger_step = self.loop.get_current_interval()
        if self.verbose:
            print(
                f"[AsyncAnnealingCallback] 异步退火回调已启动，"
                f"首次触发步数={self._next_trigger_step}"
            )

    def xǁAsyncAnnealingCallbackǁ_init_callback__mutmut_orig(self) -> None:
        """回调初始化：启动异步退火工作线程并设置首次触发步数。"""
        self.loop.start()
        self._next_trigger_step = self.loop.get_current_interval()
        if self.verbose:
            print(
                f"[AsyncAnnealingCallback] 异步退火回调已启动，"
                f"首次触发步数={self._next_trigger_step}"
            )

    def xǁAsyncAnnealingCallbackǁ_init_callback__mutmut_1(self) -> None:
        """回调初始化：启动异步退火工作线程并设置首次触发步数。"""
        self.loop.start()
        self._next_trigger_step = None
        if self.verbose:
            print(
                f"[AsyncAnnealingCallback] 异步退火回调已启动，"
                f"首次触发步数={self._next_trigger_step}"
            )

    def xǁAsyncAnnealingCallbackǁ_init_callback__mutmut_2(self) -> None:
        """回调初始化：启动异步退火工作线程并设置首次触发步数。"""
        self.loop.start()
        self._next_trigger_step = self.loop.get_current_interval()
        if self.verbose:
            print(
                None
            )

    @_mutmut_mutated(mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut)
    def _on_step(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_orig(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_1(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is not None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_2(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = None

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_3(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls > self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_4(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = None
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_5(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(None).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_6(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.copy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_7(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    None
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_8(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(None).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_9(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = None
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_10(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls - self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_11(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return False

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_12(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = None
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_13(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(None, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_14(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, None)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_15(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_16(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, )
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_17(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = None
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_18(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = None
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_19(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls - interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_20(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        None
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_21(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = None

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_22(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls - self.loop.get_current_interval()

        return True

    def xǁAsyncAnnealingCallbackǁ_on_step__mutmut_23(self) -> bool:
        """
        每步触发：到达自适应间隔时提交退火任务

        提交操作只把模型引用放入队列，耗时在毫秒级，不会阻塞训练。
        """
        if self._next_trigger_step is None:
            self._next_trigger_step = self.loop.get_current_interval()

        if self.n_calls >= self._next_trigger_step:
            # 在主线程中快速复制一份策略网络快照，再提交到异步队列
            # 这样工作线程不需要访问正在前向传播的训练模型，避免竞争
            try:
                policy_snapshot = copy.deepcopy(self.model.policy).cpu().eval()
            except Exception as e:
                logger.error(
                    f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                    f"复制策略网络快照失败 ({type(e).__name__}: {e})"
                )
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()
                return True

            submitted = self.loop.submit(policy_snapshot, self.n_calls)
            if submitted:
                interval = self.loop.get_current_interval()
                self._next_trigger_step = self.n_calls + interval
                if self.verbose:
                    print(
                        f"[AsyncAnnealingCallback] 步数 {self.n_calls}: "
                        f"已提交退火任务，下次触发={self._next_trigger_step}"
                    )
            else:
                # 队列满时，稍后再试（下一个间隔再次尝试）
                self._next_trigger_step = self.n_calls + self.loop.get_current_interval()

        return False

    @_mutmut_mutated(mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut)
    def _on_rollout_start(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_orig(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_1(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = None
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_2(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is not None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_3(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = None
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_4(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["XXstate_dictXX"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_5(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["STATE_DICT"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_6(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = None
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_7(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["XXstepXX"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_8(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["STEP"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_9(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = None

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_10(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["XXdeltaXX"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_11(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["DELTA"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_12(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(None, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_13(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=None)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_14(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_15(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, )
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_16(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=True)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_17(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    None
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(e).__name__}: {e})"
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_18(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                None
            )

    def xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_19(self) -> None:
        """
        每个 rollout 开始前触发：回写已完成的优化权重

        训练在 rollout 之间自然存在同步点，此时加载权重不会与梯度更新冲突。
        """
        result = self.loop.get_pending_result()
        if result is None:
            return

        state_dict = result["state_dict"]
        step = result["step"]
        delta = result["delta"]

        try:
            self.model.policy.load_state_dict(state_dict, strict=False)
            if self.verbose:
                print(
                    f"[AsyncAnnealingCallback] rollout 开始前回写退火权重 "
                    f"(step={step}, delta={delta:.4f})"
                )
        except Exception as e:
            logger.error(
                f"[AsyncAnnealingCallback] 回写退火权重失败 "
                f"(step={step}, {type(None).__name__}: {e})"
            )

    @_mutmut_mutated(mutants_xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut)
    def _on_training_end(self) -> None:
        """训练结束时关闭异步退火工作线程。"""
        self.loop.shutdown(wait=True)
        if self.verbose:
            print("[AsyncAnnealingCallback] 异步退火工作线程已关闭")

    def xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_orig(self) -> None:
        """训练结束时关闭异步退火工作线程。"""
        self.loop.shutdown(wait=True)
        if self.verbose:
            print("[AsyncAnnealingCallback] 异步退火工作线程已关闭")

    def xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_1(self) -> None:
        """训练结束时关闭异步退火工作线程。"""
        self.loop.shutdown(wait=None)
        if self.verbose:
            print("[AsyncAnnealingCallback] 异步退火工作线程已关闭")

    def xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_2(self) -> None:
        """训练结束时关闭异步退火工作线程。"""
        self.loop.shutdown(wait=False)
        if self.verbose:
            print("[AsyncAnnealingCallback] 异步退火工作线程已关闭")

    def xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_3(self) -> None:
        """训练结束时关闭异步退火工作线程。"""
        self.loop.shutdown(wait=True)
        if self.verbose:
            print(None)

    def xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_4(self) -> None:
        """训练结束时关闭异步退火工作线程。"""
        self.loop.shutdown(wait=True)
        if self.verbose:
            print("XX[AsyncAnnealingCallback] 异步退火工作线程已关闭XX")

    def xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_5(self) -> None:
        """训练结束时关闭异步退火工作线程。"""
        self.loop.shutdown(wait=True)
        if self.verbose:
            print("[asyncannealingcallback] 异步退火工作线程已关闭")

    def xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_6(self) -> None:
        """训练结束时关闭异步退火工作线程。"""
        self.loop.shutdown(wait=True)
        if self.verbose:
            print("[ASYNCANNEALINGCALLBACK] 异步退火工作线程已关闭")

mutants_xǁAsyncAnnealingCallbackǁ__init____mutmut['_mutmut_orig'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ__init____mutmut['xǁAsyncAnnealingCallbackǁ__init____mutmut_1'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ__init____mutmut['xǁAsyncAnnealingCallbackǁ__init____mutmut_2'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ__init____mutmut['xǁAsyncAnnealingCallbackǁ__init____mutmut_3'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ__init____mutmut['xǁAsyncAnnealingCallbackǁ__init____mutmut_4'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ__init____mutmut_4 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingCallbackǁ_init_callback__mutmut['_mutmut_orig'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_init_callback__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_init_callback__mutmut['xǁAsyncAnnealingCallbackǁ_init_callback__mutmut_1'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_init_callback__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_init_callback__mutmut['xǁAsyncAnnealingCallbackǁ_init_callback__mutmut_2'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_init_callback__mutmut_2 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['_mutmut_orig'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_1'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_2'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_3'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_4'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_5'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_6'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_7'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_8'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_9'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_10'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_11'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_12'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_13'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_14'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_15'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_16'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_17'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_17 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_18'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_18 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_19'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_19 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_20'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_20 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_21'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_21 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_22'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_22 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_step__mutmut['xǁAsyncAnnealingCallbackǁ_on_step__mutmut_23'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_step__mutmut_23 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['_mutmut_orig'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_1'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_2'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_3'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_4'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_5'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_6'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_7'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_8'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_9'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_10'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_11'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_12'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_13'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_14'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_15'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_16'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_17'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_17 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_18'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_18 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut['xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_19'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_rollout_start__mutmut_19 # type: ignore # mutmut generated

mutants_xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut['_mutmut_orig'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut['xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_1'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut['xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_2'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut['xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_3'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut['xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_4'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut['xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_5'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut['xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_6'] = AsyncAnnealingCallback.xǁAsyncAnnealingCallbackǁ_on_training_end__mutmut_6 # type: ignore # mutmut generated


if __name__ == "__main__":
    print("AsyncAnnealingCallback 模块已加载，请配合 AsyncAnnealingLoop 使用")
