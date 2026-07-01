"""pytest 配置：注册自定义标记。"""

import pytest


def pytest_configure(config):
    """注册 benchmark 标记，避免 --strict-markers 报错。"""
    config.addinivalue_line("markers", "benchmark: marks performance benchmark tests")
