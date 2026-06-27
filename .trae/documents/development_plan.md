# 量子RL调度系统 - 后续开发实施计划

## 1. 项目现状分析

### 1.1 当前代码状态

| 模块 | 文件 | 行数 | 状态 | 备注 |
|------|------|------|------|------|
| Mock API | `src/api/mock_client.py` | 510 | ✅ 已测试 | 功能完整 |
| API 客户端 | `src/api/tianyan_client.py` | 574 | ✅ Mock委托实现 | 真实模式待实现 |
| 任务解析器 | `src/scheduler/parser.py` | 816 | ⚠️ 待验证 | Task类、解析逻辑已实现 |
| 调度环境 | `src/scheduler/env.py` | 720 | ⚠️ 待验证 | Gymnasium环境框架已搭建 |
| RL智能体 | `src/scheduler/agent.py` | 592 | ⚠️ 待验证 | Dueling DQN框架已搭建 |
| 量子退火 | `src/quantum/annealing.py` | 682 | ⚠️ 待验证 | QUBO映射框架已搭建 |
| Web界面 | `src/visualization/app.py` | 1109 | ⚠️ 待验证 | FastAPI框架已搭建 |
| 工具函数 | `src/utils/helpers.py` | 285 | ⚠️ 待验证 | 基础工具函数 |
| 快速训练 | `scripts/quick_train.py` | 63 | ✅ 已创建 | 5000步训练验证 |

### 1.2 关键问题

1. **端到端验证缺失**：各模块独立存在，但未经过完整训练流程验证
2. **状态/动作空间定义**：env.py和agent.py的接口需要对齐
3. **奖励函数实现**：env.py中的奖励计算逻辑需要验证
4. **量子退火集成**：annealing.py需要与agent.py集成
5. **单元测试不足**：tests/目录仅有一个空测试文件

---

## 2. 开发优先级

基于项目开发计划和代码状态，确定以下优先级顺序：

| 优先级 | 模块 | 任务 | 依赖 |
|--------|------|------|------|
| P0 | scheduler/env.py | 验证调度环境功能完整性 | 无 |
| P0 | scheduler/agent.py | 验证DQN智能体训练流程 | env.py |
| P1 | scripts/quick_train.py | 端到端训练验证（5000步） | env.py, agent.py |
| P1 | scheduler/parser.py | 验证任务解析器 | 无 |
| P2 | quantum/annealing.py | 量子退火集成到训练流程 | agent.py |
| P2 | api/tianyan_client.py | 真实API模式实现 | 平台权限 |
| P3 | visualization/app.py | Web监控界面验证 | env.py, agent.py |
| P3 | tests/ | 编写单元测试 | 各模块 |

---

## 3. 详细实施计划

### 阶段一：核心模块验证（P0优先级）

#### 任务 3.1：验证调度环境 `src/scheduler/env.py`

**目标**：确保 Gymnasium 环境接口完整，状态/动作/奖励逻辑正确

**修改文件**：
- `src/scheduler/env.py` - 可能需要修复bug或补充缺失逻辑

**关键检查点**：
1. `__init__` 方法：状态空间、动作空间定义正确
2. `reset` 方法：返回初始状态和 info
3. `step` 方法：动作执行、状态更新、奖励计算、终止条件
4. `render` 方法（可选）：可视化输出
5. `close` 方法：资源清理

**验证方式**：
```python
from src.scheduler.env import QuantumSchedulingEnv
env = QuantumSchedulingEnv(max_qubits=20)
obs, info = env.reset()
assert obs.shape == (8,)
obs, reward, terminated, truncated, info = env.step(0)
```

---

#### 任务 3.2：验证RL智能体 `src/scheduler/agent.py`

**目标**：确保 DQN 智能体训练、评估、保存/加载功能正常

**修改文件**：
- `src/scheduler/agent.py` - 可能需要修复bug或补充缺失逻辑

**关键检查点**：
1. `__init__` 方法：DQN模型初始化、参数配置
2. `train` 方法：训练流程、回调函数、日志记录
3. `evaluate` 方法：评估指标计算（平均奖励、成功率）
4. `save`/`load` 方法：模型持久化
5. `predict` 方法：推理接口

**验证方式**：
```python
from src.scheduler.env import QuantumSchedulingEnv
from src.scheduler.agent import SchedulerAgent
env = QuantumSchedulingEnv(max_qubits=20)
agent = SchedulerAgent(env)
model = agent.train(total_timesteps=1000)
result = agent.evaluate(num_episodes=3)
```

---

### 阶段二：端到端训练验证（P1优先级）

#### 任务 3.3：运行快速训练脚本

**目标**：通过 `scripts/quick_train.py` 验证完整训练流程

**修改文件**：
- `scripts/quick_train.py` - 确保与当前env.py和agent.py接口兼容

**验证步骤**：
1. 运行 `python scripts/quick_train.py`
2. 检查训练日志输出
3. 验证模型保存成功
4. 检查评估结果（平均奖励、成功率）

---

#### 任务 3.4：验证任务解析器 `src/scheduler/parser.py`

**目标**：确保QASM解析、Task构建、特征提取功能正常

**修改文件**：
- `src/scheduler/parser.py` - 可能需要修复bug

**关键检查点**：
1. `TaskParser.parse_qasm()` - QASM格式解析
2. `TaskBuilder` - 任务构建器
3. 特征向量提取逻辑

**验证方式**：
```python
from src.scheduler.parser import TaskParser, TaskBuilder
parser = TaskParser()
task = parser.parse_qasm(qasm_string)
```

---

### 阶段三：量子退火集成（P2优先级）

#### 任务 3.5：量子退火模块集成

**目标**：将量子退火优化器集成到RL训练流程中

**修改文件**：
- `src/quantum/annealing.py` - 验证QUBO求解器
- `src/scheduler/agent.py` - 添加量子加速接口

**关键检查点**：
1. `QuantumAnnealingOptimizer.solve_qubo()` - QUBO求解
2. 与agent.py的集成方式（策略搜索加速）
3. 仿真模式验证（无需D-Wave SDK）

---

### 阶段四：API客户端完善（P2优先级）

#### 任务 3.6：真实API模式实现

**目标**：实现天衍云真实API调用逻辑（待平台权限获取后）

**修改文件**：
- `src/api/tianyan_client.py` - 实现真实API调用

**关键检查点**：
1. 认证机制（Bearer Token）
2. 任务提交接口
3. 状态查询接口
4. 错误处理

---

### 阶段五：可视化与测试（P3优先级）

#### 任务 3.7：Web监控界面验证

**目标**：启动并验证FastAPI监控界面

**修改文件**：
- `src/visualization/app.py` - 修复启动问题

**验证方式**：
```bash
uvicorn src.visualization.app:app --reload --port 8000
```

---

#### 任务 3.8：编写单元测试

**目标**：为核心模块添加单元测试

**新建文件**：
- `tests/test_env.py` - 调度环境测试
- `tests/test_agent.py` - RL智能体测试
- `tests/test_parser.py` - 任务解析器测试
- `tests/test_api.py` - API客户端测试

---

## 4. 风险与应对措施

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| env.py/agent.py接口不匹配 | 训练失败 | 先验证接口一致性 |
| DQN训练不收敛 | 算法效果差 | 调整超参数、检查奖励函数 |
| 量子退火求解器依赖缺失 | 功能不可用 | 先使用仿真模式开发 |
| 平台权限未获取 | 无法真机测试 | 使用Mock模式完成开发 |

---

## 5. 验证标准

| 模块 | 验证标准 |
|------|----------|
| env.py | 可正常reset和step，状态维度正确 |
| agent.py | 可正常训练、评估、保存模型 |
| quick_train.py | 完整运行5000步训练，输出评估结果 |
| parser.py | 成功解析QASM并生成Task对象 |
| annealing.py | 成功求解QUBO问题（仿真模式） |
| app.py | 成功启动Web服务（port 8000） |

---

## 6. 开发流程规范

### 6.1 Git工作流
- 每个任务创建独立分支：`feature/verify-env`、`feature/verify-agent`等
- Commit格式：`<type>: <描述>`
- 使用GitHub MCP提交代码

### 6.2 代码规范
- Python ≥3.10，使用type hints
- 中文注释，函数必须有docstring
- 类名PascalCase，函数/变量snake_case
- 使用Black格式化（line-length=88）

### 6.3 验证流程
1. 开发完成后运行相关测试
2. 使用GitHub MCP提交到远程仓库
3. 在AGENTS.md中更新开发进度

---

## 7. 下一步行动

**立即执行**：
1. 验证 `src/scheduler/env.py` 的Gymnasium接口完整性
2. 验证 `src/scheduler/agent.py` 的DQN训练流程
3. 运行 `scripts/quick_train.py` 完成端到端验证

**后续跟进**：
4. 验证任务解析器和量子退火模块
5. 编写单元测试
6. 完善Web监控界面

---

> 📅 **制定日期**：2026年6月27日  
> 📋 **状态**：待批准执行