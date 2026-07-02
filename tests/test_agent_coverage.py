"""
补充 agent.py 的测试覆盖率
目标：将 agent.py 从 69% 提升到 85%+
"""
import json
import os
import tempfile
import time
import random
from unittest.mock import Mock, patch, MagicMock
from typing import Any

import gymnasium as gym
import numpy as np
import pytest
import torch as th
from gymnasium import spaces
from stable_baselines3 import DQN, PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from src.scheduler.agent import (
    SchedulerAgent,
    AnnealingCallback,
    RealMachineCallback,
)


class TestSchedulerAgentEvaluation:
    """测试 SchedulerAgent.evaluate() 方法"""

    def test_evaluate_without_model_raises_error(self):
        """测试未训练时调用 evaluate() 应抛出 RuntimeError"""
        env = gym.make("CartPole-v1")
        agent = SchedulerAgent(env)

        with pytest.raises(RuntimeError, match="模型尚未训练"):
            agent.evaluate(num_episodes=3)


class TestSchedulerAgentSave:
    """测试 SchedulerAgent.save() 方法"""

    def test_save_without_model_raises_error(self):
        """测试未训练时调用 save() 应抛出 RuntimeError"""
        env = gym.make("CartPole-v1")
        agent = SchedulerAgent(env)

        with pytest.raises(RuntimeError, match="没有可保存的模型"):
            agent.save("test_model")


class TestSchedulerAgentLoad:
    """测试 SchedulerAgent.load() 方法"""

    def test_load_model(self):
        """测试加载已保存的模型"""
        env = gym.make("CartPole-v1")
        agent = SchedulerAgent(env)
        agent.train(total_timesteps=100)

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = os.path.join(tmpdir, "test_model")
            agent.save(model_path)

            agent2 = SchedulerAgent(env)
            agent2.load(model_path)

            obs = env.reset()[0]
            action1 = agent.predict(obs)
            action2 = agent2.predict(obs)
            assert action1 == action2


class TestAnnealingCallback:
    """测试 AnnealingCallback"""

    def test_callback_initialization(self):
        """测试回调初始化"""
        mock_optimizer = Mock()
        callback = AnnealingCallback(
            optimizer=mock_optimizer,
            interval=500,
            verbose=1,
            head_only=True
        )

        assert callback.interval == 500
        assert callback.verbose == 1
        assert callback.head_only is True
        assert callback.best_reward == -float("inf")
        assert callback.optimized_count == 0

    def test_callback_on_step_no_trigger(self):
        """测试未达到间隔时不触发优化"""
        mock_optimizer = Mock()
        callback = AnnealingCallback(
            optimizer=mock_optimizer,
            interval=1000,
            verbose=0
        )

        callback.n_calls = 500
        result = callback._on_step()
        assert result is True
        mock_optimizer.optimize_policy.assert_not_called()

    def test_callback_on_step_with_exception(self):
        """测试优化抛出异常时回调正常处理"""
        mock_optimizer = Mock()
        mock_optimizer.optimize_policy.side_effect = Exception("Annealing failed")

        callback = AnnealingCallback(
            optimizer=mock_optimizer,
            interval=100,
            verbose=1
        )

        callback.n_calls = 100
        result = callback._on_step()
        assert result is True


class TestRealMachineCallback:
    """测试 RealMachineCallback"""

    def test_callback_initialization(self):
        """测试回调初始化"""
        mock_env = Mock()
        mock_env._real_clients = {}

        callback = RealMachineCallback(
            env=mock_env,
            interval=500,
            prob=0.05,
            save_path="test_results.json",
            shots=1024,
            verbose=1
        )

        assert callback.interval == 500
        assert callback.prob == 0.05
        assert callback.shots == 1024
        assert callback.verbose == 1
        assert callback._warned_no_client is False

    def test_callback_no_client_warns_once(self):
        """测试无客户端时仅警告一次"""
        mock_env = Mock()
        mock_env._real_clients = {}

        callback = RealMachineCallback(
            env=mock_env,
            interval=100,
            prob=1.0,
            verbose=0  # 关闭verbose避免输出
        )

        # 第一次调用：应该设置 _warned_no_client = True
        callback.n_calls = 100
        result = callback._on_step()
        assert result is True
        assert callback._warned_no_client is True

        # 第二次调用：_warned_no_client 应该保持 True（不会重复警告）
        result = callback._on_step()
        assert result is True
        assert callback._warned_no_client is True  # 应该是 True，不是 False

    def test_callback_probability_gate(self):
        """测试概率门控"""
        mock_env = Mock()
        mock_env._real_clients = {}

        callback = RealMachineCallback(
            env=mock_env,
            interval=100,
            prob=0.0,  # 0% 概率
            verbose=0
        )

        callback.n_calls = 100
        result = callback._on_step()
        assert result is True

    def test_callback_skip_when_prob_not_met(self):
        """测试概率未命中时跳过"""
        mock_env = Mock()
        mock_env._real_clients = {"mock_machine": Mock()}

        callback = RealMachineCallback(
            env=mock_env,
            interval=100,
            prob=0.0,  # 永远不会触发
            verbose=0
        )

        with patch("random.random", return_value=0.5):
            callback.n_calls = 100
            result = callback._on_step()
            assert result is True

    def test_callback_training_end_saves_results(self):
        """测试训练结束时保存结果"""
        mock_env = Mock()
        mock_env._real_clients = {}

        with tempfile.TemporaryDirectory() as tmpdir:
            save_path = os.path.join(tmpdir, "real_times.json")
            callback = RealMachineCallback(
                env=mock_env,
                interval=100,
                prob=0.05,
                save_path=save_path,
                verbose=0
            )

            callback.real_times = [
                {"step": 100, "task_id": "test1", "status": "submitted"}
            ]

            callback._on_training_end()

            assert os.path.exists(save_path)
            with open(save_path, "r") as f:
                data = json.load(f)
                assert len(data) == 1
                assert data[0]["task_id"] == "test1"

    def test_callback_training_end_no_save_path(self):
        """测试无保存路径时不保存"""
        mock_env = Mock()
        mock_env._real_clients = {}

        callback = RealMachineCallback(
            env=mock_env,
            interval=100,
            prob=0.05,
            save_path="",
            verbose=0
        )

        callback.real_times = [{"step": 100}]
        callback._on_training_end()  # Should not raise


class TestSchedulerAgentGetConfig:
    """测试 SchedulerAgent.get_config() 方法"""

    def test_get_config_returns_correct_keys(self):
        """测试配置字典包含正确的键"""
        env = gym.make("CartPole-v1")
        agent = SchedulerAgent(env)
        config = agent.get_config()

        expected_keys = [
            "observation_dim", "action_dim", "learning_rate",
            "buffer_size", "batch_size", "gamma",
            "target_update_interval", "train_freq",
            "epsilon_start", "epsilon_end", "epsilon_decay",
            "learning_starts", "tau", "log_dir", "net_arch",
            "architecture"
        ]

        for key in expected_keys:
            assert key in config, f"Missing key: {key}"


class TestSchedulerAgentRepr:
    """测试 SchedulerAgent.__repr__() 方法"""

    def test_repr_returns_string(self):
        """测试 __repr__ 返回非空字符串"""
        env = gym.make("CartPole-v1")
        agent = SchedulerAgent(env)
        repr_str = repr(agent)

        assert isinstance(repr_str, str)
        assert len(repr_str) > 0
        assert "SchedulerAgent" in repr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
