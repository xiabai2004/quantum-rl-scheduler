# 量子RL驱动的天衍云平台智能调度系统

> 2026 年“揭榜挂帅”擂台赛参赛项目
> 方向：量子 AI 双向赋能的研究与应用探索
> 目标平台：天衍云平台真机“天衍-287”

本项目面向量子云平台的任务调度问题，构建一个由强化学习驱动的智能调度系统：用 AI 决策量子/经典资源分配，用量子退火加速策略搜索，让异构任务在多台量子机器之间更高效地排队、分流和执行。

## 项目亮点

| 方向 | 当前能力 |
| --- | --- |
| AI 赋能量子计算 | PPO/DQN 调度智能体，支持量子、经典、混合任务分流 |
| 量子赋能 AI | QUBO 映射与量子退火优化器，用于辅助策略搜索 |
| 多机器调度 | 支持 3 台异构量子机器的自动选择与负载分配 |
| 真机验证 | 已完成天衍云多机器任务提交验证 |
| 可视化 | FastAPI + Vue3 + Echarts 监控界面 |

核心指标目标：

- 资源利用率提升 30% 以上
- 平均等待时间降低 40% 以上
- 支持 Mock 开发与真实天衍云 API 切换

## 架构总览

```text
FastAPI Web 监控界面
    |
    +-- src/scheduler/      调度环境、任务解析、PPO/DQN 智能体
    +-- src/quantum/        QUBO 映射与量子退火优化
    +-- src/api/            天衍云 API、cqlib 真机客户端、Mock 客户端
    +-- src/visualization/  后端接口与前端页面
    +-- scripts/            训练、仿真、真机验证、报告生成
    +-- tests/              单元测试与集成测试
```

## 快速开始

默认使用 Mock 模式，不需要 API Key，也不会访问真实量子云平台。

```bash
git clone https://github.com/xiabai2004/quantum-rl-scheduler.git
cd quantum-rl-scheduler

python -m venv venv

# Windows PowerShell
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python -m pytest tests/ -v
```

最小导入验证：

```bash
python -c "from src.scheduler.env import QuantumSchedulingEnv; print('OK')"
```

## 常用命令

```bash
# Mock API 功能测试
python scripts/test_mock_api.py

# 端到端集成测试
python scripts/e2e_test.py

# 快速训练验证
python scripts/quick_train.py

# 策略仿真对比
python scripts/run_simulation.py --mock-mode --num-tasks 200

# 多机器调度演示
python scripts/demo_multi_machine.py --episodes 20

# 启动 Web 监控界面
uvicorn src.visualization.app:app --reload --port 8000
```

## 关键模块

| 模块 | 文件 | 说明 |
| --- | --- | --- |
| 调度环境 | `src/scheduler/env.py` | Gymnasium 环境，10 维状态，多机器调度 |
| RL 智能体 | `src/scheduler/agent.py` | PPO 主力算法，DQN 备选算法 |
| 任务解析 | `src/scheduler/parser.py` | QASM/JSON/文本任务解析与标准化 |
| 量子退火 | `src/quantum/annealing.py` | QUBO 构造、能量计算、退火求解 |
| API 客户端 | `src/api/` | Mock、天衍云 API、cqlib 真机客户端 |
| 可视化 | `src/visualization/` | FastAPI 后端与 Vue3 前端 |

## 当前进展

项目已完成从 Mock 开发、PPO 策略验证到多机器真机提交验证的主流程。

| 能力 | 状态 |
| --- | --- |
| Mock API 客户端 | 已完成 |
| 调度环境与任务解析 | 已完成 |
| PPO/DQN 智能体 | 已完成 |
| QUBO 与量子退火模块 | 已完成 |
| 多机器调度 | 已完成 |
| 天衍云真机提交验证 | 已完成 |
| Web 监控界面 | 已完成 |
| 参赛材料 | 准备中 |

近期重点是完善参赛材料、演示视频、答辩 PPT 和最终提交文档。

## 文档入口

| 文档 | 适合谁看 | 内容 |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | AI 助手、协作者 | 项目全貌、架构、接口速查、开发约定 |
| [新人上手指南](docs/新人上手指南.md) | 新队友 | 环境搭建、领取任务、日常开发流程 |
| [队友协同开发指南](docs/队友协同开发指南.md) | 所有开发者 | 分支、提交、PR 协作流程 |
| [Git 工作流](docs/Git工作流.md) | 需要提交代码的人 | Git 操作规范与常见问题 |
| [团队分工](docs/团队分工.md) | 项目管理 | 角色职责与任务分配 |
| [开发计划](docs/开发计划.md) | 项目管理、答辩准备 | 时间线和阶段目标 |
| [Docker 部署](docs/docker-deploy.md) | 部署人员 | 容器化运行说明 |

## 开发约定

- 默认保持 `config/config.yaml` 中 `tianyan.mock_mode: true`
- 不提交 `.env`、API Key、虚拟环境、模型文件和缓存目录
- Python 版本要求 3.10 及以上
- 代码格式使用 Black，建议行宽 88
- 函数和类需要 docstring
- `main` 分支受保护，日常开发通过功能分支和 Pull Request 合并

提交格式：

```text
feat: 添加任务优先级队列
fix: 修复 QUBO 矩阵维度错误
docs: 更新 README 快速开始
test: 添加多机器调度测试
```

## 许可证

项目知识产权与参赛材料按赛事规则执行。代码许可证见 [LICENSE](LICENSE)。
