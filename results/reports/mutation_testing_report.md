# Mutation Testing 基线报告

**生成时间**: 2026-07-01  
**工具**: mutmut v3.6.0  
**配置**: `pyproject.toml` 中 `[tool.mutmut]`  
**状态**: ⚠️ 待执行（需要在 Linux/WSL 环境中运行）

---

## 执行环境要求

mutmut 不支持 Windows 原生环境，需要在 WSL 或 Linux 中执行：

```bash
# 1. 进入 WSL 环境
wsl bash

# 2. 创建虚拟环境并安装依赖
cd /mnt/c/Users/HZR/Desktop/揭榜挂帅擂台赛/quantum-rl-scheduler
python3 -m venv .venv-mutmut
source .venv-mutmut/bin/activate
pip install -r requirements.txt
pip install mutmut pytest pytest-cov

# 3. 执行 mutation testing（分模块避免超时）
mutmut run src/scheduler/env.py
mutmut run src/scheduler/marl.py
mutmut run src/api/tianyan_client.py

# 4. 查看结果
mutmut results
```

---

## 预期结果格式

### 模块 1: src/scheduler/env.py

**文件描述**: Gymnasium 调度环境（14维状态空间，异质化任务生成，多机器调度）  
**代码行数**: ~1,100 行  
**测试覆盖**: test_scheduler.py, test_state_space.py

| 指标 | 预期值 | 说明 |
|------|--------|------|
| 总变异数 | 150-200 | 基于代码复杂度和分支数量 |
| 杀死变异数 | 90-120 | 测试用例应覆盖核心逻辑 |
| 存活变异数 | 60-80 | 需要补充测试的场景 |
| Mutation Score | 60-70% | 基线目标，不要求达到 80% |

**预期存活变异热点**:
- 边界条件处理（如 `max_qubits` 验证）
- 异常降级路径（如机器不可用时的回退逻辑）
- 多机器负载均衡的启发式算法

---

### 模块 2: src/scheduler/marl.py

**文件描述**: MAPPO 多智能体调度（MultiAgentEnvWrapper + MAPPO 训练循环）  
**代码行数**: 952 行  
**测试覆盖**: test_marl.py（18 用例）

| 指标 | 预期值 | 说明 |
|------|--------|------|
| 总变异数 | 120-160 | 多智能体逻辑复杂 |
| 杀死变异数 | 70-90 | 测试覆盖单机/双机/三机场景 |
| 存活变异数 | 50-70 | 边缘场景测试不足 |
| Mutation Score | 55-65% | 基线目标 |

**预期存活变异热点**:
- 机器动态加入/离线场景
- 集中式 Critic 的全局状态拼接逻辑
- 奖励分配机制（shapley value 等）

---

### 模块 3: src/api/tianyan_client.py

**文件描述**: 天衍云 API 客户端（含熔断器、重试、Mock 切换）  
**代码行数**: 633 行  
**测试覆盖**: test_api.py（129 用例，95.96% 覆盖率）

| 指标 | 预期值 | 说明 |
|------|--------|------|
| 总变异数 | 80-100 | API 调用逻辑 + 熔断器 |
| 杀死变异数 | 65-80 | 高覆盖率测试 |
| 存活变异数 | 15-20 | 异常路径和超时场景 |
| Mutation Score | 75-85% | 测试覆盖最完善的模块 |

**预期存活变异热点**:
- 熔断器状态转换边界（HALF_OPEN → CLOSED 的临界条件）
- 重试次数耗尽后的降级逻辑
- Mock 模式与真实模式的切换分支

---

## 假阳性变异识别指南

以下类型的变异可能是"假阳性"（合理的代码写法但 mutmut 判定为存活）：

1. **日志消息修改**
   ```python
   # 原始代码
   logger.info("Task scheduled successfully")
   # 变异后
   logger.info("XXTask scheduled successfullyXX")
   ```
   **判定**: 假阳性。日志消息不影响业务逻辑，测试不应依赖日志内容。

2. **注释和文档字符串**
   ```python
   # 原始代码
   """计算任务等待时间"""
   # 变异后
   """XX计算任务等待时间XX"""
   ```
   **判定**: 假阳性。文档字符串不影响运行时行为。

3. **类型注解修改**
   ```python
   # 原始代码
   def process(task: Task) -> Result:
   # 变异后
   def process(task: Task) -> None:
   ```
   **判定**: 假阳性。类型注解在运行时被忽略（除非使用 `typing.get_type_hints`）。

4. **变量名重命名（不影响逻辑）**
   ```python
   # 原始代码
   timeout = 30
   # 变异后
   timeout = 31
   ```
   **判定**: 需人工审查。如果测试未覆盖超时边界，则为真阳性；如果测试明确验证超时值，则为假阳性。

---

## 后续改进计划

基于 mutation testing 结果，优先补充以下测试：

1. **env.py 存活变异**
   - 补充边界条件测试（`max_qubits=0`, `max_steps=-1`）
   - 补充多机器负载均衡的极端场景（所有机器不可用）

2. **marl.py 存活变异**
   - 补充机器动态加入/离线的时序测试
   - 补充奖励分配的边界条件（所有任务失败）

3. **tianyan_client.py 存活变异**
   - 补充熔断器状态转换的精确时序测试
   - 补充重试次数耗尽后的降级验证

---

## 执行记录

| 时间 | 操作 | 结果 |
|------|------|------|
| 2026-07-01 | 配置 mutmut v3.6.0 | ✅ 完成 |
| 2026-07-01 | 更新 pyproject.toml | ✅ `source_paths` 替代 `paths_to_mutate` |
| 2026-07-01 | WSL 环境依赖安装 | ⏳ 进行中（网络较慢） |
| - | 执行 env.py mutation testing | ⏳ 待执行 |
| - | 执行 marl.py mutation testing | ⏳ 待执行 |
| - | 执行 tianyan_client.py mutation testing | ⏳ 待执行 |
| - | 更新本报告的实际数据 | ⏳ 待执行 |

---

## 参考命令

```bash
# 查看某个变异的详细信息
mutmut show <mutant_id>

# 应用某个变异到源代码（用于调试）
mutmut apply <mutant_id>

# 导出所有存活变异
mutmut results --only-surviving > surviving_mutants.txt

# 针对特定文件重新运行
mutmut run src/scheduler/env.py --rerun
```

---

**备注**: 本报告为基线模板，实际数据需要在 Linux/WSL 环境中执行 `mutmut run` 后更新。目标不是达到 80% mutation score，而是建立基线数据，指导后续测试改进。
