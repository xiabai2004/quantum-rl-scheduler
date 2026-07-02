# AGENTS.md — 量子RL调度系统项目通用记忆

> 此文件供所有 AI Agent（CodeBuddy / TRAE / Claude / Cursor 等）读取，以快速理解项目全貌。
> 每次重要变更后请更新本文档的"最后更新"日期和对应章节。

**最后更新**：2026-07-01（v7：Track A 工程收尾完成 + Track B 比赛材料完成 + v1 技术提升全面落地）

***

## 开始工作前必读

### Git 推送规则

| 你是谁        | 怎么推送                                                     |
| ---------- | -------------------------------------------------------- |
| **普通队友**   | 创建功能分支 → `git push origin feature/xxx` → 创建 PR → 1人审批后合并 |
| **管理员/瑞哥** | `git push origin main`（GitHub 原生分支保护已启用）                 |

**Commit 格式**：

```
<type>: <简短描述>
feat / fix / docs / test / refactor / chore
```

***

## 1. 项目概述

**作品名称**：量子RL驱动的天衍云平台智能调度系统
**所属比赛**：2026年"揭榜挂帅"擂台赛 — 榜题"量子AI双向赋能的研究与应用探索"
**主办方**：共青团中央主办 / 中国电信发榜 / 中电信量子执行
**团队人数**：8人（含负责人）
**负责人**：瑞哥（GitHub: xiabai2004）

**核心创新—双向赋能**：
- AI 赋能 量子计算：用强化学习（RL）智能调度量子/经典任务
- 量子 赋能 AI：用量子退火（QUBO映射）加速 RL 决策
- 量化目标：资源利用率提升 ≥30%，平均等待时间降低 ≥40%

**目标平台**：天衍云平台真机"天衍-287"（287量子比特超导量子计算机）

**仓库地址**：<https://github.com/xiabai2004/quantum-rl-scheduler>

## 2. 关键时间节点

| 日期         | 事项     | 状态      |
| ---------- | ------ | ------- |
| 2026-06-30 | 报名截止   | 已通过 |
| 2026-07-01 | Track A 工程收尾 / Track B 比赛材料 | 已完成 |
| 2026-09-15 | 作品提交截止 | 📅 |
| 2026-09-30 | 初审结果公布 | 📅 |
| 2026-11    | 终审擂台赛  | 📅 |

## 3. 项目代码结构（v7）

```
quantum-rl-scheduler/
├── AGENTS.md                     # 本文档
├── README.md                     # 项目介绍 + 快速开始
├── requirements.txt              # Python 依赖清单
├── pyproject.toml                # 统一配置（Black/ruff/bandit/mypy/pytest/coverage/mutmut）
├── mypy.ini                      # 类型检查（8项严格配置，2模块暂时豁免）
├── .editorconfig                 # 跨编辑器编码风格统一
├── .pre-commit-config.yaml       # Git pre-commit 自动检查
├── .env.example                  # 环境变量模板
├── CONTRIBUTING.md               # 贡献指南
├── Dockerfile + docker-compose.yml  # 一键部署

├── src/                          # 源代码（22 文件，~11,000 行）
│   ├── exceptions.py             # 统一异常体系（8类）
│   ├── scheduler/                # 调度引擎（核心模块）
│   │   ├── parser.py             # 量子任务解析（700行）
│   │   ├── env.py                # Gymnasium调度环境（14维/异质化/多机器）
│   │   ├── agent.py              # PPO + DQN 双智能体（含LSTM变体）
│   │   ├── marl.py               # MAPPO 多智能体调度（952行）
│   │   ├── multi_objective_env.py # 多目标奖励包装器（306行）
│   │   └── async_annealing_callback.py # 异步退火回调（108行）
│   ├── api/
│   │   ├── tianyan_client.py     # 天衍云 API 客户端（633行）
│   │   ├── tianyan_cqlib.py      # cqlib 真机客户端 + 多机器协调器
│   │   ├── mock_client.py        # Mock API 客户端
│   │   └── circuit_breaker.py    # 熔断器（CLOSED/OPEN/HALF_OPEN）
│   ├── quantum/
│   │   ├── annealing.py          # 量子退火优化器（1094行）
│   │   └── annealing_loop.py     # 异步退火闭环控制器（294行）
│   ├── visualization/
│   │   └── app.py               # FastAPI Web 监控界面（1349行）
│   └── utils/
│       ├── helpers.py            # 工具函数
│       └── metrics.py            # Prometheus 7个指标

├── tests/                        # 测试（14 文件，100+ 用例）
│   ├── test_scheduler.py         # 调度环境测试
│   ├── test_marl.py              # MAPPO 测试
│   ├── test_annealing.py         # 量子退火测试
│   ├── test_annealing_loop.py    # 异步退火闭环测试
│   ├── test_multi_objective.py   # 多目标奖励测试
│   ├── test_state_space.py       # 状态空间测试
│   ├── test_api.py               # API 层测试
│   ├── test_parser.py            # 解析器测试
│   ├── test_visualization.py     # 可视化测试
│   ├── test_helpers.py           # 工具函数测试
│   ├── test_property.py          # property-based testing
│   └── benchmarks/test_annealing_benchmark.py  # 性能基准

├── scripts/                      # 按功能分区（v7 重组）
│   ├── cli.py                    # Click 统一入口（train/simulate/serve/demo）
│   ├── training/                 # train_agent.py, quick_train.py
│   ├── evaluation/               # run_simulation.py, hyperparameter_search.py, run_experiments.py
│   ├── demo/                     # demo.py, demo_cqlib.py, demo_multi_machine.py
│   ├── testing/                  # e2e_test.py, calibrate_mock.py, verify_annealing_real.py
│   ├── benchmarking/             # mock_vs_real.py, stress_test.py, efficient_real_benchmark.py
│   └── reporting/                # generate_report.py

├── docs/
│   ├── 新人上手指南.md            # 团队 onboarding
│   ├── 队友协同开发指南.md         # 精简版快速上手
│   ├── Git工作流.md              # 分支管理规范
│   ├── 团队分工.md               # 角色职责
│   ├── 开发计划.md               # 详细时间线
│   └── 项目记忆_给AI.md           # AI 助手同步记忆文件

├── results/reports/              # 实验数据固化报告
│   ├── strategy_comparison.md    # 8策略对比
│   ├── ablation_report.md        # 消融实验
│   ├── stress_test_report.md     # 压力测试
│   └── real_machine_validation.md # 真机验证

├── 比赛材料（workspace 根目录）
│   ├── 答辩PPT大纲.md
│   ├── 答辩PPT_量子RL调度系统.pptx  # 15页完整PPT
│   ├── 技术白皮书_更新计划.md
│   ├── 技术白皮书_量子RL调度系统_v2.docx  # 10章完整白皮书
│   └── 演示视频分镜脚本.md          # 6段5分钟

├── .github/
│   └── workflows/
│       ├── ci.yml                  # CI 4 Job：lint→test→typecheck→benchmarks
│       └── pr-automation.yml       # PR 自动标签 + Commit 格式校验
│   └── dependabot.yml             # 自动依赖更新

└── config/
    ├── .env.example
    └── config.yaml
```

## 4. 技术栈

| 层级  | 技术                     | 用途               |
| --- | ---------------------- | ---------------- |
| 语言  | Python 3.10+                | 全部               |
| RL  | Stable-Baselines3 (PPO/DQN/MAPPO)    | 双算法 + 多智能体    |
| RL  | Gymnasium              | 环境封装             |
| DL  | PyTorch ≥2.0                | 神经网络             |
| 量子  | 天衍云 cqlib SDK              | 287量子比特超导处理器 |
| 量子  | D-Wave dimod / neal             | 量子退火           |
| Web | FastAPI + Uvicorn      | 监控界面             |
| 前端  | Vue3 + Echarts         | 监控面板             |
| CLI | Click | 统一命令行入口 |
| 可观测 | Prometheus | 7个指标（Gauge/Counter/Histogram） |
| 代码质量 | ruff(10类) + mypy(8项) + bandit | v1技术提升方案 |
| CI | GitHub Actions 4 Job + Codecov + Dependabot | 自动化质量门禁 |

## 5. v1 技术提升方案落地成果

### 代码质量强化
- mypy：8项严格配置（disallow_untyped_defs + disallow_incomplete_defs + warn_return_any + strict_equality 等），2模块暂时豁免
- ruff：完全替代 flake8，10类规则集（E/W/F/I/N/B/SIM/C4/UP/RUF）
- bandit：安全扫描集成到 CI lint job

### 工程韧性
- 统一异常体系：8类异常（QuantumSchedulerError → 5子类），code + retryable 语义
- API 熔断器：CLOSED/OPEN/HALF_OPEN 三态转换
- Prometheus 指标：7个指标覆盖调度/API/退火三个维度
- Click CLI：train/simulate/serve/demo 四子命令统一入口

### 测试升级
- 测试文件：5 → 14（+9 个专用测试模块）
- 测试代码量：2,462 → 4,485 行（+82%）
- CI 强制覆盖率：40% → 60%
- 新增：property-based testing + 性能基准测试 + mutation testing 配置

### CI/CD 增强
- 4 Job 流水线：lint(ruff+bandit) + test(3.10/3.11/3.12) + typecheck(mypy) + benchmarks
- Dependabot：pip + GitHub Actions 双生态系统自动更新
- pre-commit：Git commit 自动检查 + Commit 格式校验

## 6. v7 实验成果

| 实验 | 核心结论 |
|------|---------|
| 8策略对比 | PPO奖励2864 vs FCFS 1466，+95.4%（公平对比环境，14维状态） |
| 五维消融 | D4多机+86.3% > D1算法+95.4% > D5退火+6.4% > D2状态+2.1% |
| 压力测试 | 4场景PPO综合稳定性最强；量子波动场景PPO +91.4% |
| 真机验证 | 32任务100%成功率；Mock校准后偏差<5% |

详见 `results/reports/` 目录。

## 7. 比赛材料

| 材料 | 路径 | 状态 |
|------|------|------|
| 答辩PPT（15页） | `../答辩PPT_量子RL调度系统.pptx` | 已完成 |
| 技术白皮书（10章） | `../技术白皮书_量子RL调度系统_v2.docx` | 已完成 |
| 演示视频分镜脚本 | `演示视频分镜脚本.md` | 已完成 |
| 演示视频（5分钟） | — | 待录制 |

## 8. 当前进度

```
v1 技术提升   █████████████████   83%（缺 pre-commit ruff+bandit迁移）
Track A       ████████████████████ 100%
Track B       ████████████████████ 100%（PPT/白皮书/视频脚本/实验数据）
Track C       ████████░░░░░░░░░░   40%（mypy豁免清理+覆盖率80%+mutation testing 待执行）
GitHub Issues           ██████      8 个待创建 issue（已写好模板）
真机闭环       ░░░░░░░░░░░░░░░░░░   0%（PPO cqlib 注入待开发）
```

## 9. 下一步

- Track C：mypy 豁免 6→2 + 覆盖率 40→60% + mutation testing 基线
- GitHub Issues：创建 8 个新 issue
- PPO 真机闭环：cqlib 注入调度循环（最高价值 feature）
- 视频录制：5分钟演示视频

详见 workspace 根目录 `下一步开发方向_v2.md`、`TrackC_提示词_给TRAE.md`、`GitHub_Issues_待创建.md`。

## 10. 团队信息

| GitHub 用户名      | 权限    |
| --------------- | ----- |
| xiabai2004      | Admin |
| heka-ky         | Write |
| zyhsga          | Write |
| NN2914          | Write |
| qpqpalalzmzm112 | Write |
| Jackhock-1      | Write |
| DUMNOX          | Write |
| K1660729        | Write |

## 11. 快速命令参考

```bash
# ── CLI 统一入口 ──
python scripts/cli.py train --timesteps 50000 --algorithm ppo
python scripts/cli.py simulate --num-tasks 200 --strategies all
python scripts/cli.py serve --port 8000
python scripts/cli.py demo --multi-machine

# ── 代码质量 ──
ruff check src/ scripts/ tests/           # 代码检查
ruff format src/ scripts/ tests/          # 代码格式化
mypy src/                                  # 类型检查
bandit -r src/ -c pyproject.toml -ll      # 安全扫描
pre-commit run --all-files                 # pre-commit 全量检查

# ── 测试 ──
pytest tests/ --cov=src --cov-fail-under=60  # 测试 + 覆盖率
pytest tests/benchmarks/ --benchmark-only    # 性能基准

# ── Web ──
uvicorn src.visualization.app:app --reload --port 8000

# ── Docker ──
docker-compose up -d
```
