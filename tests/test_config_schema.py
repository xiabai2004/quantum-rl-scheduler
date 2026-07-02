"""
配置 Schema 验证测试
Tests for src/config/schema.py (Pydantic config validation)
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pydantic import ValidationError

from src.config.schema import AppConfig, validate_and_print, validate_config


class TestAppConfigValidation(unittest.TestCase):
    """AppConfig Schema 基础校验。"""

    def test_validates_minimal_config(self):
        """仅提供 scheduler.algorithm 的最简配置应通过校验。"""
        cfg = AppConfig(scheduler={"algorithm": "DQN"})
        self.assertEqual(cfg.scheduler.algorithm, "DQN")
        self.assertEqual(cfg.scheduler.learning_rate, 3e-4)
        self.assertEqual(cfg.scheduler.gamma, 0.99)

    def test_default_values(self):
        """空配置应使用所有默认值。"""
        cfg = AppConfig()
        self.assertEqual(cfg.scheduler.algorithm, "DQN")
        self.assertEqual(cfg.quantum.backend, "tianyan-287")
        self.assertEqual(cfg.quantum.max_qubits, 287)
        self.assertEqual(cfg.tianyan.mock_mode, True)
        self.assertEqual(cfg.web.port, 8000)

    def test_rejects_invalid_algorithm(self):
        """非法的 algorithm 值应抛出 ValidationError。"""
        with self.assertRaises(ValidationError):
            AppConfig(scheduler={"algorithm": "INVALID"})

    def test_rejects_negative_learning_rate(self):
        """负学习率应抛出 ValidationError。"""
        with self.assertRaises(ValidationError):
            AppConfig(scheduler={"learning_rate": -0.1})

    def test_rejects_extra_top_level_field(self):
        """顶层未知字段（extra="forbid"）应抛出 ValidationError。"""
        with self.assertRaises(ValidationError):
            AppConfig(typo_field=123)

    def test_rejects_port_out_of_range(self):
        """端口号超出范围应抛出 ValidationError。"""
        with self.assertRaises(ValidationError):
            AppConfig(web={"port": 99999})

    def test_accepts_valid_port(self):
        """合法端口号应通过校验。"""
        cfg = AppConfig(web={"port": 3000})
        self.assertEqual(cfg.web.port, 3000)


class TestValidateConfig(unittest.TestCase):
    """validate_config 函数测试。"""

    def test_returns_appconfig_on_valid(self):
        """合法配置应返回 AppConfig 实例。"""
        result = validate_config({"scheduler": {"algorithm": "PPO"}})
        self.assertIsInstance(result, AppConfig)
        self.assertEqual(result.scheduler.algorithm, "PPO")

    def test_raises_on_invalid(self):
        """非法配置应抛出 ValidationError。"""
        with self.assertRaises(ValidationError):
            validate_config({"scheduler": {"algorithm": "BAD"}})

    def test_handles_real_config_structure(self):
        """真实 config.yaml 结构的配置应通过校验。"""
        data = {
            "tianyan": {"mock_mode": True, "timeout": 30},
            "scheduler": {"algorithm": "DQN", "learning_rate": 3e-4},
            "quantum": {"backend": "tianyan-287", "max_qubits": 287},
            "annealing": {"enabled": True, "num_qubits": 10},
            "cache": {"type": "redis", "host": "localhost"},
            "classical": {"max_cpu_utilization": 0.95},
            "database": {"type": "sqlite", "path": "data/scheduler.db"},
            "system": {"log_level": "INFO", "max_steps": 1000},
            "web": {"port": 8000},
        }
        cfg = validate_config(data)
        self.assertEqual(cfg.scheduler.algorithm, "DQN")


class TestValidateAndPrint(unittest.TestCase):
    """validate_and_print 函数测试。"""

    def test_returns_appconfig_on_valid(self):
        """应返回 AppConfig 且不抛异常。"""
        result = validate_and_print({"scheduler": {"algorithm": "DQN"}})
        self.assertIsInstance(result, AppConfig)

    def test_raises_on_invalid(self):
        """非法配置应抛出 ValidationError。"""
        with self.assertRaises(ValidationError):
            validate_and_print({"scheduler": {"algorithm": "NOPE"}})


if __name__ == "__main__":
    unittest.main()
