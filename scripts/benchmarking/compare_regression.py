#!/usr/bin/env python3
"""
Benchmark 回归检测脚本
Benchmark Regression Comparison Script

比较两个 pytest-benchmark 输出的 JSON 文件，检测性能退化。

用法:
    python scripts/benchmarking/compare_regression.py <current.json> [baseline.json]
    python scripts/benchmarking/compare_regression.py benchmark_results.json

若无 baseline.json，仅输出当前结果摘要（用于 baseline 生成）。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
REGRESSION_THRESHOLD_PCT = 10.0  # 退化阈值（%），超过此值输出告警
WARN_COLOR = "\033[93m"
RED_COLOR = "\033[91m"
GREEN_COLOR = "\033[92m"
RESET_COLOR = "\033[0m"


def _load_json(path: str) -> dict:
    """加载 JSON 文件，处理文件不存在错误。"""
    path = Path(path)
    if not path.exists():
        print(f"错误：文件不存在 — {path}")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _build_index(entries: list[dict]) -> dict[str, float]:
    """从 benchmark JSON entries 构建 {name: mean_time} 索引。"""
    index: dict[str, float] = {}
    for entry in entries:
        name = entry.get("name", entry.get("fullname", "unknown"))
        stats = entry.get("stats", {})
        mean = stats.get("mean", stats.get("min", 0))
        index[name] = mean
    return index


def print_summary(data: dict) -> None:
    """打印 benchmark 结果摘要。"""
    entries = data.get("benchmarks", [])
    if not entries:
        print("无 benchmark 数据。")
        return

    print(f"\n{'Benchmark':<60} {'Mean (ms)':<12}")
    print("-" * 72)
    for entry in entries:
        name = entry.get("name", entry.get("fullname", "?"))
        stats = entry.get("stats", {})
        mean_ms = stats.get("mean", 0) * 1000
        print(f"  {name:<58} {mean_ms:>10.4f}")
    print()


def compare(current_path: str, baseline_path: str) -> int:
    """
    比较 current 和 baseline 的 benchmark 结果。

    Returns:
        0 如果无退化超标，1 如果有退化超过阈值。
    """
    current_data = _load_json(current_path)
    baseline_data = _load_json(baseline_path)

    current_idx = _build_index(current_data.get("benchmarks", []))
    baseline_idx = _build_index(baseline_data.get("benchmarks", []))

    if not current_idx:
        print("当前结果中无 benchmark 条目。")
        return 0
    if not baseline_idx:
        print("基线结果中无 benchmark 条目，跳过比较。")
        print_summary(current_data)
        return 0

    print(f"\n{'Benchmark':<50} {'基线(ms)':<12} {'当前(ms)':<12} {'变化%':<10} {'状态':<10}")
    print("-" * 96)

    regressions: list[tuple[str, float, float, float]] = []
    new_entries: list[str] = []
    removed_entries: list[str] = []

    all_names = set(current_idx.keys()) | set(baseline_idx.keys())

    for name in sorted(all_names):
        if name not in current_idx:
            removed_entries.append(name)
            continue
        if name not in baseline_idx:
            new_entries.append(name)
            continue

        cur = current_idx[name] * 1000
        base = baseline_idx[name] * 1000
        if base == 0:
            continue

        change_pct = ((cur - base) / base) * 100

        if change_pct > REGRESSION_THRESHOLD_PCT:
            status = f"{RED_COLOR}⚠ 退化{RESET_COLOR}"
            regressions.append((name, cur, base, change_pct))
        elif change_pct > 0:
            status = "稍慢"
        elif change_pct < -REGRESSION_THRESHOLD_PCT:
            status = f"{GREEN_COLOR}✓ 优化{RESET_COLOR}"
        else:
            status = "稳定"

        print(f"  {name:<48} {base:>10.4f} {cur:>10.4f} {change_pct:>+8.1f}%{''.ljust(3)}{status}")

    # 新增/移除条目
    if new_entries:
        print(f"\n{WARN_COLOR}新增 benchmark 条目 ({len(new_entries)}):{RESET_COLOR}")
        for e in new_entries:
            print(f"  + {e}")

    if removed_entries:
        print(f"\n{WARN_COLOR}移除 benchmark 条目 ({len(removed_entries)}):{RESET_COLOR}")
        for e in removed_entries:
            print(f"  - {e}")

    # 退化汇总
    if regressions:
        print(f"\n{RED_COLOR}⚠ 发现 {len(regressions)} 个性能退化超过 {REGRESSION_THRESHOLD_PCT}% 的条目:{RESET_COLOR}")
        for name, cur, base, pct in regressions:
            print(f"  {RED_COLOR}{name}: {base:.4f}ms → {cur:.4f}ms ({pct:+.1f}%){RESET_COLOR}")
        print(f"\n{RED_COLOR}建议：检查对应代码变更，确认是否为预期退化。{RESET_COLOR}")
        return 1
    else:
        print(f"\n{GREEN_COLOR}✓ 未发现性能退化超过 {REGRESSION_THRESHOLD_PCT}% 的条目。{RESET_COLOR}")
        return 0


def main() -> None:
    """CLI 入口。"""
    if len(sys.argv) < 2:
        print("用法: python compare_regression.py <current.json> [baseline.json]")
        print("      若只提供一个文件，输出结果摘要（用于生成基线）。")
        sys.exit(0)

    current_path = sys.argv[1]

    if len(sys.argv) >= 3:
        baseline_path = sys.argv[2]
        exit_code = compare(current_path, baseline_path)
    else:
        data = _load_json(current_path)
        print_summary(data)
        exit_code = 0

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
