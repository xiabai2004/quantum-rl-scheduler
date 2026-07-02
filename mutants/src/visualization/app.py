"""
Web可视化监控界面
Web Visualization Monitoring Dashboard

基于 FastAPI + 原生 HTML/JS 的量子RL调度系统监控界面
支持 WebSocket 实时推送、手动任务提交、调度策略切换等功能

运行方式:
    python src/visualization/app.py
    或
    python -m src.visualization.app
"""

import asyncio
import json
import os
import sys
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncGenerator

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# 确保项目根目录在 Python 路径中
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


# ============================================================
# 数据模型定义
# ============================================================


class TaskSubmit(BaseModel):
    """提交新任务的请求体"""

    user_id: str = Field(default="user_001", description="用户ID")
    task_type: str = Field(default="quantum", description="任务类型: quantum/classical/hybrid")
    priority: int = Field(default=3, ge=1, le=5, description="优先级 1-5")
    qubit_count: int = Field(default=10, ge=1, description="所需量子比特数")
    circuit_depth: int = Field(default=100, ge=1, description="电路深度")
    estimated_time: float = Field(default=60.0, ge=0.1, description="预计执行时间(秒)")


class SystemStatusUpdate(BaseModel):
    """系统状态更新请求体（供调度引擎调用）"""

    qubit_utilization: float = Field(default=0.0, ge=0.0, le=1.0)
    queue_length: int = Field(default=0, ge=0)
    completed_tasks: int = Field(default=0, ge=0)
    average_wait_time: float = Field(default=0.0, ge=0.0)


# ============================================================
# 内存存储（生产环境应替换为 Redis 等外部存储）
# ============================================================

# 当前系统状态
system_status: dict = {
    "qubit_utilization": 0.65,  # 量子比特利用率 (0~1)
    "queue_length": 5,  # 任务队列长度
    "average_wait_time": 12.3,  # 平均等待时间(秒)
    "completed_tasks": 42,  # 已完成任务数
    "current_step": 1024,  # 当前调度步数
    "current_strategy": "PPO-Balanced",  # 当前调度策略
    "strategy_options": [  # 可选策略列表
        "DQN-Reward",
        "DQN-Latency",
        "PPO-Balanced",
        "QAOA-Hybrid",
        "FCFS",
    ],
    "real_machines": [],  # 真机列表 [{name, status, type, id}]
    "real_submissions": [],  # 真机提交记录 [{step, task_id, machine, latency_s, status}]
    "last_update": datetime.now().isoformat(),
}

# 任务队列
task_queue: list[dict] = [
    {
        "task_id": "QTASK-" + uuid.uuid4().hex[:6],
        "user_id": "user_001",
        "task_type": "quantum",
        "status": "pending",
        "priority": 4,
        "qubit_count": 12,
        "circuit_depth": 150,
        "estimated_time": 45.0,
        "arrival_time": datetime.now().isoformat(),
    },
    {
        "task_id": "QTASK-" + uuid.uuid4().hex[:6],
        "user_id": "user_002",
        "task_type": "hybrid",
        "status": "pending",
        "priority": 3,
        "qubit_count": 8,
        "circuit_depth": 80,
        "estimated_time": 30.0,
        "arrival_time": datetime.now().isoformat(),
    },
    {
        "task_id": "QTASK-" + uuid.uuid4().hex[:6],
        "user_id": "user_001",
        "task_type": "classical",
        "status": "pending",
        "priority": 2,
        "qubit_count": 0,
        "circuit_depth": 0,
        "estimated_time": 20.0,
        "arrival_time": datetime.now().isoformat(),
    },
]
mutants_xǁConnectionManagerǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁConnectionManagerǁconnect__mutmut: MutantDict = {}  # type: ignore
mutants_xǁConnectionManagerǁdisconnect__mutmut: MutantDict = {}  # type: ignore
mutants_xǁConnectionManagerǁbroadcast__mutmut: MutantDict = {}  # type: ignore


# WebSocket 连接管理器
class ConnectionManager:
    """管理所有 WebSocket 客户端连接"""

    @_mutmut_mutated(mutants_xǁConnectionManagerǁ__init____mutmut)
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    def xǁConnectionManagerǁ__init____mutmut_orig(self) -> None:
        self.active_connections: list[WebSocket] = []

    def xǁConnectionManagerǁ__init____mutmut_1(self) -> None:
        self.active_connections: list[WebSocket] = None

    @_mutmut_mutated(mutants_xǁConnectionManagerǁconnect__mutmut)
    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    async def xǁConnectionManagerǁconnect__mutmut_orig(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    async def xǁConnectionManagerǁconnect__mutmut_1(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(None)

    @_mutmut_mutated(mutants_xǁConnectionManagerǁdisconnect__mutmut)
    def disconnect(self, websocket: WebSocket) -> None:
        """断开 WebSocket 连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    def xǁConnectionManagerǁdisconnect__mutmut_orig(self, websocket: WebSocket) -> None:
        """断开 WebSocket 连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    def xǁConnectionManagerǁdisconnect__mutmut_1(self, websocket: WebSocket) -> None:
        """断开 WebSocket 连接"""
        if websocket not in self.active_connections:
            self.active_connections.remove(websocket)

    def xǁConnectionManagerǁdisconnect__mutmut_2(self, websocket: WebSocket) -> None:
        """断开 WebSocket 连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(None)

    @_mutmut_mutated(mutants_xǁConnectionManagerǁbroadcast__mutmut)
    async def broadcast(self, message: dict) -> None:
        """向所有连接的客户端广播消息"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

    async def xǁConnectionManagerǁbroadcast__mutmut_orig(self, message: dict) -> None:
        """向所有连接的客户端广播消息"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

    async def xǁConnectionManagerǁbroadcast__mutmut_1(self, message: dict) -> None:
        """向所有连接的客户端广播消息"""
        disconnected = None
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

    async def xǁConnectionManagerǁbroadcast__mutmut_2(self, message: dict) -> None:
        """向所有连接的客户端广播消息"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(None)
            except Exception:
                disconnected.append(connection)
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

    async def xǁConnectionManagerǁbroadcast__mutmut_3(self, message: dict) -> None:
        """向所有连接的客户端广播消息"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(None)
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

    async def xǁConnectionManagerǁbroadcast__mutmut_4(self, message: dict) -> None:
        """向所有连接的客户端广播消息"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        for conn in disconnected:
            if conn not in self.active_connections:
                self.active_connections.remove(conn)

    async def xǁConnectionManagerǁbroadcast__mutmut_5(self, message: dict) -> None:
        """向所有连接的客户端广播消息"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(None)

mutants_xǁConnectionManagerǁ__init____mutmut['_mutmut_orig'] = ConnectionManager.xǁConnectionManagerǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁConnectionManagerǁ__init____mutmut['xǁConnectionManagerǁ__init____mutmut_1'] = ConnectionManager.xǁConnectionManagerǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁConnectionManagerǁconnect__mutmut['_mutmut_orig'] = ConnectionManager.xǁConnectionManagerǁconnect__mutmut_orig # type: ignore # mutmut generated
mutants_xǁConnectionManagerǁconnect__mutmut['xǁConnectionManagerǁconnect__mutmut_1'] = ConnectionManager.xǁConnectionManagerǁconnect__mutmut_1 # type: ignore # mutmut generated

mutants_xǁConnectionManagerǁdisconnect__mutmut['_mutmut_orig'] = ConnectionManager.xǁConnectionManagerǁdisconnect__mutmut_orig # type: ignore # mutmut generated
mutants_xǁConnectionManagerǁdisconnect__mutmut['xǁConnectionManagerǁdisconnect__mutmut_1'] = ConnectionManager.xǁConnectionManagerǁdisconnect__mutmut_1 # type: ignore # mutmut generated
mutants_xǁConnectionManagerǁdisconnect__mutmut['xǁConnectionManagerǁdisconnect__mutmut_2'] = ConnectionManager.xǁConnectionManagerǁdisconnect__mutmut_2 # type: ignore # mutmut generated

mutants_xǁConnectionManagerǁbroadcast__mutmut['_mutmut_orig'] = ConnectionManager.xǁConnectionManagerǁbroadcast__mutmut_orig # type: ignore # mutmut generated
mutants_xǁConnectionManagerǁbroadcast__mutmut['xǁConnectionManagerǁbroadcast__mutmut_1'] = ConnectionManager.xǁConnectionManagerǁbroadcast__mutmut_1 # type: ignore # mutmut generated
mutants_xǁConnectionManagerǁbroadcast__mutmut['xǁConnectionManagerǁbroadcast__mutmut_2'] = ConnectionManager.xǁConnectionManagerǁbroadcast__mutmut_2 # type: ignore # mutmut generated
mutants_xǁConnectionManagerǁbroadcast__mutmut['xǁConnectionManagerǁbroadcast__mutmut_3'] = ConnectionManager.xǁConnectionManagerǁbroadcast__mutmut_3 # type: ignore # mutmut generated
mutants_xǁConnectionManagerǁbroadcast__mutmut['xǁConnectionManagerǁbroadcast__mutmut_4'] = ConnectionManager.xǁConnectionManagerǁbroadcast__mutmut_4 # type: ignore # mutmut generated
mutants_xǁConnectionManagerǁbroadcast__mutmut['xǁConnectionManagerǁbroadcast__mutmut_5'] = ConnectionManager.xǁConnectionManagerǁbroadcast__mutmut_5 # type: ignore # mutmut generated


manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期：启动时开启后台模拟任务"""
    task = asyncio.create_task(simulate_scheduler())
    yield
    task.cancel()


# ============================================================
# FastAPI 应用实例
# ============================================================

app = FastAPI(title="量子RL调度系统监控界面", version="1.0.0", lifespan=lifespan)


# ============================================================
# 页面路由：返回监控面板 HTML
# ============================================================

# 获取前端 HTML 文件路径
import os as _os

FRONTEND_HTML_PATH = _os.path.join(_os.path.dirname(__file__), "frontend", "index.html")

# 缓存前端 HTML 内容
_VUE3_HTML_TEMPLATE = None
mutants_x__load_vue3_template__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__load_vue3_template__mutmut)
def _load_vue3_template() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(FRONTEND_HTML_PATH, encoding="utf-8") as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_orig() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(FRONTEND_HTML_PATH, encoding="utf-8") as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_1() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is not None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(FRONTEND_HTML_PATH, encoding="utf-8") as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_2() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(None):
            with open(FRONTEND_HTML_PATH, encoding="utf-8") as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_3() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(None, encoding="utf-8") as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_4() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(FRONTEND_HTML_PATH, encoding=None) as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_5() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(encoding="utf-8") as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_6() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(FRONTEND_HTML_PATH, ) as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_7() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(FRONTEND_HTML_PATH, encoding="XXutf-8XX") as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_8() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(FRONTEND_HTML_PATH, encoding="UTF-8") as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_9() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(FRONTEND_HTML_PATH, encoding="utf-8") as f:
                _VUE3_HTML_TEMPLATE = None
        else:
            _VUE3_HTML_TEMPLATE = HTML_TEMPLATE  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE


def x__load_vue3_template__mutmut_10() -> str:
    """加载 Vue3 前端 HTML 模板"""
    global _VUE3_HTML_TEMPLATE
    if _VUE3_HTML_TEMPLATE is None:
        if _os.path.exists(FRONTEND_HTML_PATH):
            with open(FRONTEND_HTML_PATH, encoding="utf-8") as f:
                _VUE3_HTML_TEMPLATE = f.read()
        else:
            _VUE3_HTML_TEMPLATE = None  # 回退到旧的 HTML
    return _VUE3_HTML_TEMPLATE

mutants_x__load_vue3_template__mutmut['_mutmut_orig'] = x__load_vue3_template__mutmut_orig # type: ignore # mutmut generated
mutants_x__load_vue3_template__mutmut['x__load_vue3_template__mutmut_1'] = x__load_vue3_template__mutmut_1 # type: ignore # mutmut generated
mutants_x__load_vue3_template__mutmut['x__load_vue3_template__mutmut_2'] = x__load_vue3_template__mutmut_2 # type: ignore # mutmut generated
mutants_x__load_vue3_template__mutmut['x__load_vue3_template__mutmut_3'] = x__load_vue3_template__mutmut_3 # type: ignore # mutmut generated
mutants_x__load_vue3_template__mutmut['x__load_vue3_template__mutmut_4'] = x__load_vue3_template__mutmut_4 # type: ignore # mutmut generated
mutants_x__load_vue3_template__mutmut['x__load_vue3_template__mutmut_5'] = x__load_vue3_template__mutmut_5 # type: ignore # mutmut generated
mutants_x__load_vue3_template__mutmut['x__load_vue3_template__mutmut_6'] = x__load_vue3_template__mutmut_6 # type: ignore # mutmut generated
mutants_x__load_vue3_template__mutmut['x__load_vue3_template__mutmut_7'] = x__load_vue3_template__mutmut_7 # type: ignore # mutmut generated
mutants_x__load_vue3_template__mutmut['x__load_vue3_template__mutmut_8'] = x__load_vue3_template__mutmut_8 # type: ignore # mutmut generated
mutants_x__load_vue3_template__mutmut['x__load_vue3_template__mutmut_9'] = x__load_vue3_template__mutmut_9 # type: ignore # mutmut generated
mutants_x__load_vue3_template__mutmut['x__load_vue3_template__mutmut_10'] = x__load_vue3_template__mutmut_10 # type: ignore # mutmut generated


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """返回监控面板 HTML 页面（Vue3 + Echarts 版本）"""
    return HTMLResponse(content=_load_vue3_template())


# ============================================================
# API 路由
# ============================================================


@app.get("/api/status")
async def get_status() -> dict:
    """获取当前系统状态（JSON）"""
    return system_status


@app.get("/api/real-machines")
async def get_real_machines() -> dict:
    """查询天衍云真实量子计算机状态（实时轮询 cqlib）。

    返回 ``[{id, type, status, name}]``，其中 status 为
    running/calibrating/maintenance 等真实状态。
    无 TIANYAN_API_KEY 时返回空列表。
    """
    machines = _get_real_machines_status()
    return {
        "machines": machines,
        "count": len(machines),
        "source": "cqlib" if machines else "unavailable",
    }


@app.get("/api/real-submissions")
async def get_real_submissions() -> dict:
    """查询最近的真机提交记录（从 results/real_times.json 读取）。"""
    records = _load_real_submissions()
    return {
        "submissions": records,
        "count": len(records),
    }


@app.get("/api/tasks")
async def get_tasks(status: str | None = None) -> list[dict]:
    """
    获取任务列表
    - status=pending: 只返回等待中的任务
    - status=running: 只返回运行中的任务
    - status=completed: 只返回已完成的任务
    - 不传: 返回全部任务
    """
    if status:
        return [t for t in task_queue if t["status"] == status]
    return task_queue


@app.post("/api/tasks")
async def submit_task(task: TaskSubmit) -> dict:
    """提交新任务"""
    new_task = {
        "task_id": "QTASK-" + uuid.uuid4().hex[:8],
        "user_id": task.user_id,
        "task_type": task.task_type,
        "status": "pending",
        "priority": task.priority,
        "qubit_count": task.qubit_count,
        "circuit_depth": task.circuit_depth,
        "estimated_time": task.estimated_time,
        "arrival_time": datetime.now().isoformat(),
    }
    task_queue.append(new_task)
    # 更新系统状态中的队列长度
    system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
    system_status["last_update"] = datetime.now().isoformat()
    # 广播更新
    await manager.broadcast(
        {
            "type": "task_added",
            "task": new_task,
            "status": system_status,
        }
    )
    return {"message": "任务提交成功", "task_id": new_task["task_id"]}


@app.get("/api/metrics")
async def get_metrics() -> str:
    """返回 Prometheus 格式的指标（可选功能）"""
    lines = [
        "# HELP quantum_scheduler_qubit_utilization 量子比特利用率 0~1",
        "# TYPE quantum_scheduler_qubit_utilization gauge",
        f"quantum_scheduler_qubit_utilization {system_status['qubit_utilization']:.4f}",
        "",
        "# HELP quantum_scheduler_queue_length 任务队列长度",
        "# TYPE quantum_scheduler_queue_length gauge",
        f"quantum_scheduler_queue_length {system_status['queue_length']}",
        "",
        "# HELP quantum_scheduler_completed_tasks 已完成任务总数",
        "# TYPE quantum_scheduler_completed_tasks counter",
        f"quantum_scheduler_completed_tasks {system_status['completed_tasks']}",
        "",
        "# HELP quantum_scheduler_avg_wait_time 平均等待时间(秒)",
        "# TYPE quantum_scheduler_avg_wait_time gauge",
        f"quantum_scheduler_avg_wait_time {system_status['average_wait_time']:.2f}",
        "",
        "# HELP quantum_scheduler_current_step 当前调度步数",
        "# TYPE quantum_scheduler_current_step counter",
        f"quantum_scheduler_current_step {system_status['current_step']}",
    ]
    return "\n".join(lines)


@app.post("/api/strategy")
async def switch_strategy(strategy: str) -> dict:
    """切换调度策略"""
    if strategy not in system_status["strategy_options"]:
        return {"message": f"未知策略: {strategy}", "success": False}
    old = system_status["current_strategy"]
    system_status["current_strategy"] = strategy
    system_status["last_update"] = datetime.now().isoformat()
    await manager.broadcast(
        {
            "type": "strategy_changed",
            "old_strategy": old,
            "new_strategy": strategy,
            "status": system_status,
        }
    )
    return {"message": f"策略切换: {old} -> {strategy}", "success": True}


@app.post("/api/update")
async def update_status(update: SystemStatusUpdate) -> dict:
    """更新系统状态（供调度引擎调用）"""
    system_status["qubit_utilization"] = update.qubit_utilization
    system_status["queue_length"] = update.queue_length
    system_status["completed_tasks"] = update.completed_tasks
    system_status["average_wait_time"] = update.average_wait_time
    system_status["last_update"] = datetime.now().isoformat()
    await manager.broadcast(
        {
            "type": "status_update",
            "status": system_status,
        }
    )
    return {"message": "状态更新成功", "status": system_status}


# ============================================================
# PPO 数据接口
# ============================================================

# 懒加载 PPO 模型和环境
_ppo_model = None
_ppo_env = None
mutants_x__get_ppo_model__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__get_ppo_model__mutmut)
def _get_ppo_model() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_orig() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_1() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is not None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_2() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = None
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_3() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=None, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_4() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=None)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_5() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_6() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, )
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_7() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=21, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_8() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=43)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_9() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = None

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_10() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(None, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_11() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, None, "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_12() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", None, "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_13() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", None)

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_14() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join("models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_15() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_16() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_17() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", )

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_18() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "XXmodelsXX", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_19() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "MODELS", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_20() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "XXppo_seed_42_v4XX", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_21() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "PPO_SEED_42_V4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_22() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "XXbest_model.zipXX")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_23() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "BEST_MODEL.ZIP")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_24() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_25() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(None):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_26() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = None
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_27() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(None, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_28() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, None)
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_29() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join("models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_30() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, )
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_31() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "XXmodelsXX")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_32() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "MODELS")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_33() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(None):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_34() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "XXppoXX" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_35() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "PPO" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_36() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" not in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_37() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).upper():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_38() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(None).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_39() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(None):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_40() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith("XX.zipXX"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_41() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".ZIP"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_42() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = None
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_43() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(None, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_44() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, None)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_45() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_46() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, )
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_47() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                return
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_48() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(None):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_49() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            return

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_50() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(None):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_51() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = None
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_52() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(None, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_53() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=None)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_54() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_55() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, )
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_56() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(None)
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_57() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(None)
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_58() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(None)
            _ppo_model = None
    return _ppo_model


def x__get_ppo_model__mutmut_59() -> Any:
    """加载 PPO 模型（懒加载，避免启动时阻塞）"""
    global _ppo_model, _ppo_env
    if _ppo_model is None:
        try:
            from stable_baselines3 import PPO

            from src.scheduler.env import QuantumSchedulingEnv

            _ppo_env = QuantumSchedulingEnv(max_qubits=20, seed=42)
            model_path = os.path.join(_PROJECT_ROOT, "models", "ppo_seed_42_v4", "best_model.zip")

            if not os.path.exists(model_path):
                # 自动发现：在 models/ 下找任意 ppo 开头的目录中的 best_model.zip
                models_dir = os.path.join(_PROJECT_ROOT, "models")
                for root, _dirs, files in os.walk(models_dir):
                    if "ppo" in os.path.basename(root).lower():
                        for f in files:
                            if f.endswith(".zip"):
                                model_path = os.path.join(root, f)
                                break
                        if os.path.exists(model_path):
                            break

            if os.path.exists(model_path):
                _ppo_model = PPO.load(model_path, env=_ppo_env)
                print(f"[PPO] 模型加载成功: {model_path}")
            else:
                print(f"[PPO] 模型文件不存在: {model_path}，尝试使用 DQN")
        except Exception as e:
            print(f"[PPO] 模型加载失败: {e}")
            _ppo_model = ""
    return _ppo_model

mutants_x__get_ppo_model__mutmut['_mutmut_orig'] = x__get_ppo_model__mutmut_orig # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_1'] = x__get_ppo_model__mutmut_1 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_2'] = x__get_ppo_model__mutmut_2 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_3'] = x__get_ppo_model__mutmut_3 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_4'] = x__get_ppo_model__mutmut_4 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_5'] = x__get_ppo_model__mutmut_5 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_6'] = x__get_ppo_model__mutmut_6 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_7'] = x__get_ppo_model__mutmut_7 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_8'] = x__get_ppo_model__mutmut_8 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_9'] = x__get_ppo_model__mutmut_9 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_10'] = x__get_ppo_model__mutmut_10 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_11'] = x__get_ppo_model__mutmut_11 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_12'] = x__get_ppo_model__mutmut_12 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_13'] = x__get_ppo_model__mutmut_13 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_14'] = x__get_ppo_model__mutmut_14 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_15'] = x__get_ppo_model__mutmut_15 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_16'] = x__get_ppo_model__mutmut_16 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_17'] = x__get_ppo_model__mutmut_17 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_18'] = x__get_ppo_model__mutmut_18 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_19'] = x__get_ppo_model__mutmut_19 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_20'] = x__get_ppo_model__mutmut_20 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_21'] = x__get_ppo_model__mutmut_21 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_22'] = x__get_ppo_model__mutmut_22 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_23'] = x__get_ppo_model__mutmut_23 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_24'] = x__get_ppo_model__mutmut_24 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_25'] = x__get_ppo_model__mutmut_25 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_26'] = x__get_ppo_model__mutmut_26 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_27'] = x__get_ppo_model__mutmut_27 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_28'] = x__get_ppo_model__mutmut_28 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_29'] = x__get_ppo_model__mutmut_29 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_30'] = x__get_ppo_model__mutmut_30 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_31'] = x__get_ppo_model__mutmut_31 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_32'] = x__get_ppo_model__mutmut_32 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_33'] = x__get_ppo_model__mutmut_33 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_34'] = x__get_ppo_model__mutmut_34 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_35'] = x__get_ppo_model__mutmut_35 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_36'] = x__get_ppo_model__mutmut_36 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_37'] = x__get_ppo_model__mutmut_37 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_38'] = x__get_ppo_model__mutmut_38 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_39'] = x__get_ppo_model__mutmut_39 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_40'] = x__get_ppo_model__mutmut_40 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_41'] = x__get_ppo_model__mutmut_41 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_42'] = x__get_ppo_model__mutmut_42 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_43'] = x__get_ppo_model__mutmut_43 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_44'] = x__get_ppo_model__mutmut_44 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_45'] = x__get_ppo_model__mutmut_45 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_46'] = x__get_ppo_model__mutmut_46 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_47'] = x__get_ppo_model__mutmut_47 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_48'] = x__get_ppo_model__mutmut_48 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_49'] = x__get_ppo_model__mutmut_49 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_50'] = x__get_ppo_model__mutmut_50 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_51'] = x__get_ppo_model__mutmut_51 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_52'] = x__get_ppo_model__mutmut_52 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_53'] = x__get_ppo_model__mutmut_53 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_54'] = x__get_ppo_model__mutmut_54 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_55'] = x__get_ppo_model__mutmut_55 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_56'] = x__get_ppo_model__mutmut_56 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_57'] = x__get_ppo_model__mutmut_57 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_58'] = x__get_ppo_model__mutmut_58 # type: ignore # mutmut generated
mutants_x__get_ppo_model__mutmut['x__get_ppo_model__mutmut_59'] = x__get_ppo_model__mutmut_59 # type: ignore # mutmut generated


# ============================================================
# 真机状态轮询：通过 cqlib 查询天衍云真实量子计算机状态
# ============================================================

# 懒加载真机 cqlib 客户端（仅在配置了 TIANYAN_API_KEY 时创建）
_real_cqlib_client = None
_real_cqlib_checked = False
mutants_x__get_real_cqlib_client__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__get_real_cqlib_client__mutmut)
def _get_real_cqlib_client() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_orig() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_1() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = None
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_2() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = False
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_3() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = None
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_4() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv(None, "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_5() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", None)
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_6() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_7() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", )
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_8() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("XXTIANYAN_API_KEYXX", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_9() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("tianyan_api_key", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_10() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "XXXX")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_11() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_12() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print(None)
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_13() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("XX[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用XX")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_14() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[web] 未配置 tianyan_api_key，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_15() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[WEB] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_16() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = None
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_17() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=None,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_18() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name=None,
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_19() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=None,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_20() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_21() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_22() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_23() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="XXtianyan_sXX",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_24() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="TIANYAN_S",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_25() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=False,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_26() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print(None)
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_27() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("XX[Web] 真机 cqlib 客户端已就绪: tianyan_sXX")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_28() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_29() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[WEB] 真机 CQLIB 客户端已就绪: TIANYAN_S")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_30() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(None)
        _real_cqlib_client = None
    return _real_cqlib_client


def x__get_real_cqlib_client__mutmut_31() -> Any:
    """懒加载天衍云 cqlib 客户端。

    从 .env 读取 TIANYAN_API_KEY，无 Key 时返回 None（降级为纯仿真展示）。
    客户端创建失败也返回 None，保证 Web 界面不会因真机不可达而崩溃。
    """
    global _real_cqlib_client, _real_cqlib_checked
    if _real_cqlib_checked:
        return _real_cqlib_client
    _real_cqlib_checked = True
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("TIANYAN_API_KEY", "")
        if not api_key:
            print("[Web] 未配置 TIANYAN_API_KEY，真机状态轮询已禁用")
            return None
        from src.api.tianyan_cqlib import CqlibTianyanClient

        _real_cqlib_client = CqlibTianyanClient(
            login_key=api_key,
            machine_name="tianyan_s",
            auto_retry_machine=True,
        )
        print("[Web] 真机 cqlib 客户端已就绪: tianyan_s")
    except Exception as e:
        print(f"[Web] 真机客户端创建失败 ({e})，真机状态降级为离线")
        _real_cqlib_client = ""
    return _real_cqlib_client

mutants_x__get_real_cqlib_client__mutmut['_mutmut_orig'] = x__get_real_cqlib_client__mutmut_orig # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_1'] = x__get_real_cqlib_client__mutmut_1 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_2'] = x__get_real_cqlib_client__mutmut_2 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_3'] = x__get_real_cqlib_client__mutmut_3 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_4'] = x__get_real_cqlib_client__mutmut_4 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_5'] = x__get_real_cqlib_client__mutmut_5 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_6'] = x__get_real_cqlib_client__mutmut_6 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_7'] = x__get_real_cqlib_client__mutmut_7 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_8'] = x__get_real_cqlib_client__mutmut_8 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_9'] = x__get_real_cqlib_client__mutmut_9 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_10'] = x__get_real_cqlib_client__mutmut_10 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_11'] = x__get_real_cqlib_client__mutmut_11 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_12'] = x__get_real_cqlib_client__mutmut_12 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_13'] = x__get_real_cqlib_client__mutmut_13 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_14'] = x__get_real_cqlib_client__mutmut_14 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_15'] = x__get_real_cqlib_client__mutmut_15 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_16'] = x__get_real_cqlib_client__mutmut_16 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_17'] = x__get_real_cqlib_client__mutmut_17 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_18'] = x__get_real_cqlib_client__mutmut_18 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_19'] = x__get_real_cqlib_client__mutmut_19 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_20'] = x__get_real_cqlib_client__mutmut_20 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_21'] = x__get_real_cqlib_client__mutmut_21 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_22'] = x__get_real_cqlib_client__mutmut_22 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_23'] = x__get_real_cqlib_client__mutmut_23 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_24'] = x__get_real_cqlib_client__mutmut_24 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_25'] = x__get_real_cqlib_client__mutmut_25 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_26'] = x__get_real_cqlib_client__mutmut_26 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_27'] = x__get_real_cqlib_client__mutmut_27 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_28'] = x__get_real_cqlib_client__mutmut_28 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_29'] = x__get_real_cqlib_client__mutmut_29 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_30'] = x__get_real_cqlib_client__mutmut_30 # type: ignore # mutmut generated
mutants_x__get_real_cqlib_client__mutmut['x__get_real_cqlib_client__mutmut_31'] = x__get_real_cqlib_client__mutmut_31 # type: ignore # mutmut generated
mutants_x__get_real_machines_status__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__get_real_machines_status__mutmut)
def _get_real_machines_status() -> list[dict]:
    """查询天衍云真实量子计算机列表及状态。

    调用 ``CqlibTianyanClient.list_backends()``（底层
    ``platform.query_quantum_computer_list()``），返回包含
    running/calibrating/maintenance 等真实状态的机器列表。

    Returns:
        机器字典列表 [{id, type, status, name}]；查询失败或无客户端时返回 []
    """
    client = _get_real_cqlib_client()
    if client is None:
        return []
    try:
        return client.list_backends()  # type: ignore[no-any-return]
    except Exception as e:
        print(f"[Web] 查询真机状态失败: {e}")
        return []


def x__get_real_machines_status__mutmut_orig() -> list[dict]:
    """查询天衍云真实量子计算机列表及状态。

    调用 ``CqlibTianyanClient.list_backends()``（底层
    ``platform.query_quantum_computer_list()``），返回包含
    running/calibrating/maintenance 等真实状态的机器列表。

    Returns:
        机器字典列表 [{id, type, status, name}]；查询失败或无客户端时返回 []
    """
    client = _get_real_cqlib_client()
    if client is None:
        return []
    try:
        return client.list_backends()  # type: ignore[no-any-return]
    except Exception as e:
        print(f"[Web] 查询真机状态失败: {e}")
        return []


def x__get_real_machines_status__mutmut_1() -> list[dict]:
    """查询天衍云真实量子计算机列表及状态。

    调用 ``CqlibTianyanClient.list_backends()``（底层
    ``platform.query_quantum_computer_list()``），返回包含
    running/calibrating/maintenance 等真实状态的机器列表。

    Returns:
        机器字典列表 [{id, type, status, name}]；查询失败或无客户端时返回 []
    """
    client = None
    if client is None:
        return []
    try:
        return client.list_backends()  # type: ignore[no-any-return]
    except Exception as e:
        print(f"[Web] 查询真机状态失败: {e}")
        return []


def x__get_real_machines_status__mutmut_2() -> list[dict]:
    """查询天衍云真实量子计算机列表及状态。

    调用 ``CqlibTianyanClient.list_backends()``（底层
    ``platform.query_quantum_computer_list()``），返回包含
    running/calibrating/maintenance 等真实状态的机器列表。

    Returns:
        机器字典列表 [{id, type, status, name}]；查询失败或无客户端时返回 []
    """
    client = _get_real_cqlib_client()
    if client is not None:
        return []
    try:
        return client.list_backends()  # type: ignore[no-any-return]
    except Exception as e:
        print(f"[Web] 查询真机状态失败: {e}")
        return []


def x__get_real_machines_status__mutmut_3() -> list[dict]:
    """查询天衍云真实量子计算机列表及状态。

    调用 ``CqlibTianyanClient.list_backends()``（底层
    ``platform.query_quantum_computer_list()``），返回包含
    running/calibrating/maintenance 等真实状态的机器列表。

    Returns:
        机器字典列表 [{id, type, status, name}]；查询失败或无客户端时返回 []
    """
    client = _get_real_cqlib_client()
    if client is None:
        return []
    try:
        return client.list_backends()  # type: ignore[no-any-return]
    except Exception as e:
        print(None)
        return []

mutants_x__get_real_machines_status__mutmut['_mutmut_orig'] = x__get_real_machines_status__mutmut_orig # type: ignore # mutmut generated
mutants_x__get_real_machines_status__mutmut['x__get_real_machines_status__mutmut_1'] = x__get_real_machines_status__mutmut_1 # type: ignore # mutmut generated
mutants_x__get_real_machines_status__mutmut['x__get_real_machines_status__mutmut_2'] = x__get_real_machines_status__mutmut_2 # type: ignore # mutmut generated
mutants_x__get_real_machines_status__mutmut['x__get_real_machines_status__mutmut_3'] = x__get_real_machines_status__mutmut_3 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__load_real_submissions__mutmut)
def _load_real_submissions() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_orig() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_1() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = None
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_2() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(None, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_3() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, None, "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_4() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", None)
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_5() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join("results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_6() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_7() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", )
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_8() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "XXresultsXX", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_9() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "RESULTS", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_10() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "XXreal_times.jsonXX")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_11() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "REAL_TIMES.JSON")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_12() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_13() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(None):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_14() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(None, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_15() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding=None) as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_16() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_17() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, ) as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_18() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="XXutf-8XX") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_19() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="UTF-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_20() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = None
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_21() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(None)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_22() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[+50:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_23() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-51:][::-1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_24() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::+1]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_25() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-2]
        return []
    except Exception as e:
        print(f"[Web] 加载真机提交记录失败: {e}")
        return []


def x__load_real_submissions__mutmut_26() -> list[dict]:
    """从 results/real_times.json 加载最近的真机提交记录。

    训练回调 ``RealMachineCallback`` 会把真机提交记录写入该文件。
    Web 界面读取后展示真实提交历史（步数/机器/耗时/task_id）。

    Returns:
        提交记录列表（最多保留最近 50 条）；文件不存在时返回 []
    """
    path = os.path.join(_PROJECT_ROOT, "results", "real_times.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        if isinstance(records, list):
            # 保留最近 50 条，倒序展示
            return records[-50:][::-1]
        return []
    except Exception as e:
        print(None)
        return []

mutants_x__load_real_submissions__mutmut['_mutmut_orig'] = x__load_real_submissions__mutmut_orig # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_1'] = x__load_real_submissions__mutmut_1 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_2'] = x__load_real_submissions__mutmut_2 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_3'] = x__load_real_submissions__mutmut_3 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_4'] = x__load_real_submissions__mutmut_4 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_5'] = x__load_real_submissions__mutmut_5 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_6'] = x__load_real_submissions__mutmut_6 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_7'] = x__load_real_submissions__mutmut_7 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_8'] = x__load_real_submissions__mutmut_8 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_9'] = x__load_real_submissions__mutmut_9 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_10'] = x__load_real_submissions__mutmut_10 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_11'] = x__load_real_submissions__mutmut_11 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_12'] = x__load_real_submissions__mutmut_12 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_13'] = x__load_real_submissions__mutmut_13 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_14'] = x__load_real_submissions__mutmut_14 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_15'] = x__load_real_submissions__mutmut_15 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_16'] = x__load_real_submissions__mutmut_16 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_17'] = x__load_real_submissions__mutmut_17 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_18'] = x__load_real_submissions__mutmut_18 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_19'] = x__load_real_submissions__mutmut_19 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_20'] = x__load_real_submissions__mutmut_20 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_21'] = x__load_real_submissions__mutmut_21 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_22'] = x__load_real_submissions__mutmut_22 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_23'] = x__load_real_submissions__mutmut_23 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_24'] = x__load_real_submissions__mutmut_24 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_25'] = x__load_real_submissions__mutmut_25 # type: ignore # mutmut generated
mutants_x__load_real_submissions__mutmut['x__load_real_submissions__mutmut_26'] = x__load_real_submissions__mutmut_26 # type: ignore # mutmut generated


@app.get("/api/ppo/comparison")
async def get_ppo_comparison() -> dict:
    """返回 PPO 与其他策略的对比数据（从 v4 报告中读取）"""
    report_dir = os.path.join(_PROJECT_ROOT, "results")
    json_files = sorted(
        [
            f
            for f in os.listdir(report_dir)
            if f.startswith("simulation_results_") and f.endswith(".json")
        ],
        reverse=True,
    )
    if not json_files:
        return {"error": "未找到仿真结果文件", "strategies": [], "ppo_rank": None}

    latest_file = os.path.join(report_dir, json_files[0])
    try:
        with open(latest_file, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {"error": f"无法读取: {latest_file}", "strategies": [], "ppo_rank": None}

    sorted_items = sorted(data.items(), key=lambda x: x[1].get("avg_reward", -9999), reverse=True)
    ppo_rank = next((i + 1 for i, (k, _) in enumerate(sorted_items) if "PPO" in k.upper()), None)

    strategies = []
    for rank, (name, metrics) in enumerate(sorted_items, 1):
        strategies.append(
            {
                "rank": rank,
                "name": name,
                "avg_reward": metrics.get("avg_reward", 0),
                "avg_wait_time": metrics.get("avg_wait_time", 0),
                "completion_rate": metrics.get("completion_rate", 0),
                "qubit_utilization": metrics.get("qubit_utilization", 0),
                "classical_utilization": metrics.get("classical_utilization", 0),
            }
        )

    return {
        "strategies": strategies,
        "ppo_rank": ppo_rank,
        "total_strategies": len(strategies),
        "data_source": json_files[0],
    }


@app.get("/api/ppo/predict")
async def ppo_predict() -> dict:
    """使用 PPO 模型对当前环境状态进行一次推理预测"""
    model = _get_ppo_model()
    if model is None:
        return {"error": "PPO 模型未加载", "action": None, "confidence": 0}

    try:
        if _ppo_env is None:
            return {"error": "PPO 环境未初始化", "action": None}
        obs = _ppo_env.reset()[0]
        action, _states = model.predict(obs, deterministic=True)

        action_map = {0: "经典资源", 1: "量子资源", 2: "混合执行"}
        return {
            "action": int(action),
            "action_name": action_map.get(int(action), "未知"),
            "observation": obs.tolist()[:5],
            "model_type": "PPO",
        }
    except Exception as e:
        return {"error": str(e), "action": None}


@app.get("/api/ppo/stats")
async def ppo_stats() -> dict:
    """返回 PPO 关键性能指标"""
    report_dir = os.path.join(_PROJECT_ROOT, "results")
    json_files = sorted(
        [
            f
            for f in os.listdir(report_dir)
            if f.startswith("simulation_results_") and f.endswith(".json")
        ],
        reverse=True,
    )
    if not json_files:
        return {"error": "未找到仿真结果"}

    try:
        with open(os.path.join(report_dir, json_files[0]), encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {"error": "无法读取结果文件"}

    ppo_data = None
    for k, v in data.items():
        if "PPO" in k.upper():
            ppo_data = v
            break

    if not ppo_data:
        return {"error": "未找到 PPO 数据"}

    # 计算排名
    sorted_items = sorted(data.items(), key=lambda x: x[1].get("avg_reward", -9999), reverse=True)
    ppo_rank = next(i + 1 for i, (k, _) in enumerate(sorted_items) if "PPO" in k.upper())
    best_name, best_data = sorted_items[0]

    return {
        "ppo": {
            "reward": ppo_data.get("avg_reward"),
            "wait_time": ppo_data.get("avg_wait_time"),
            "completion_rate": ppo_data.get("completion_rate"),
            "qubit_util": ppo_data.get("qubit_utilization"),
            "classical_util": ppo_data.get("classical_utilization"),
        },
        "ppo_rank": ppo_rank,
        "total": len(sorted_items),
        "best_strategy": best_name,
        "best_reward": best_data.get("avg_reward"),
        "vs_random": round(
            ppo_data.get("avg_reward", 0) - data.get("Random", {}).get("avg_reward", 0), 1
        ),
    }


# ============================================================
# WebSocket 路由：实时推送状态更新
# ============================================================


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    WebSocket 实时推送端点
    客户端连接后，服务端会自动推送：
    - 状态更新（status_update）
    - 新任务通知（task_added）
    - 策略变更通知（strategy_changed）
    """
    await manager.connect(websocket)
    try:
        # 连接后立即发送当前状态 + PPO 数据
        ppo_stats = {}
        try:
            report_dir = os.path.join(_PROJECT_ROOT, "results")
            json_files = sorted(
                [f for f in os.listdir(report_dir) if f.startswith("simulation_results_")],
                reverse=True,
            )
            if json_files:
                with open(os.path.join(report_dir, json_files[0])) as f:
                    sim_data = json.load(f)
                sorted_items = sorted(
                    sim_data.items(), key=lambda x: x[1].get("avg_reward", -9999), reverse=True
                )
                ppo_rank = next(
                    (i + 1 for i, (k, _) in enumerate(sorted_items) if "PPO" in k.upper()), None
                )
                ppo_stats = {"ppo_rank": ppo_rank, "total": len(sorted_items)}
        except Exception:
            pass

        await websocket.send_json(
            {
                "type": "init",
                "status": system_status,
                "tasks": task_queue,
                "ppo_stats": ppo_stats,
            }
        )
        # 保持连接，监听客户端消息（心跳/指令）
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
            except json.JSONDecodeError:
                # 忽略非 JSON 消息，避免连接断开
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Invalid JSON format",
                    }
                )
                continue
            # 客户端可发送 {"action": "ping"} 作为心跳
            if msg.get("action") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
mutants_x_simulate_scheduler__mutmut: MutantDict = {}  # type: ignore


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


@_mutmut_mutated(mutants_x_simulate_scheduler__mutmut)
async def simulate_scheduler() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_orig() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_1() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = None
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_2() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 1
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_3() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while False:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_4() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(None)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_5() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(4)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_6() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick = 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_7() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick -= 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_8() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 2
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_9() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] = 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_10() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] -= 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_11() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["XXcurrent_stepXX"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_12() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["CURRENT_STEP"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_13() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 2

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_14() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = None
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_15() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None or _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_16() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None or model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_17() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_18() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_19() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_20() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = None
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_21() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[1]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_22() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = None
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_23() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(None, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_24() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=None)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_25() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_26() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, )
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_27() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=False)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_28() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = None
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_29() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 1.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_30() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action != 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_31() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 2 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_32() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (1.4 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_33() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action != 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_34() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 3 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_35() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 1.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_36() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = None
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_37() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["XXqubit_utilizationXX"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_38() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["QUBIT_UTILIZATION"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_39() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    None, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_40() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, None
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_41() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_42() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_43() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 - target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_44() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] / 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_45() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["XXqubit_utilizationXX"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_46() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["QUBIT_UTILIZATION"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_47() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 1.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_48() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit / 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_49() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 1.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_50() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 5
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_51() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = None
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_52() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["XXqubit_utilizationXX"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_53() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["QUBIT_UTILIZATION"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_54() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    None,
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_55() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    None,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_56() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_57() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_58() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        None,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_59() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        None,
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_60() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_61() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_62() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        1.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_63() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(None, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_64() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, None),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_65() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_66() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, ),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_67() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(2.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_68() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] - random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_69() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["XXqubit_utilizationXX"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_70() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["QUBIT_UTILIZATION"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_71() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(None, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_72() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, None)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_73() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_74() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, )),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_75() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(+0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_76() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-1.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_77() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 1.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_78() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    5,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_79() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = None

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_80() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["XXqubit_utilizationXX"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_81() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["QUBIT_UTILIZATION"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_82() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                None,
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_83() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                None,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_84() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_85() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_86() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    None, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_87() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, None
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_88() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_89() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_90() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    1.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_91() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(None, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_92() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, None)
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_93() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_94() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, )
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_95() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(2.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_96() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] - random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_97() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["XXqubit_utilizationXX"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_98() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["QUBIT_UTILIZATION"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_99() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(None, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_100() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, None))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_101() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_102() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, ))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_103() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(+0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_104() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-1.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_105() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 1.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_106() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                5,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_107() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = None
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_108() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["XXqueue_lengthXX"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_109() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["QUEUE_LENGTH"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_110() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = None
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_111() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["XXaverage_wait_timeXX"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_112() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["AVERAGE_WAIT_TIME"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_113() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            None, 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_114() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), None
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_115() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_116() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_117() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(None, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_118() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, None), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_119() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_120() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, ), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_121() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(1.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_122() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] - random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_123() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["XXaverage_wait_timeXX"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_124() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["AVERAGE_WAIT_TIME"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_125() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(None, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_126() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, None)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_127() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_128() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, )), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_129() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(+0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_130() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-1.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_131() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 1.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_132() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 2
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_133() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = None

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_134() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["XXlast_updateXX"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_135() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["LAST_UPDATE"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_136() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick / 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_137() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 21 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_138() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 != 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_139() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 1:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_140() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = None
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_141() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = None
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_142() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["XXreal_machinesXX"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_143() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["REAL_MACHINES"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_144() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(None)
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_145() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = None
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_146() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["XXreal_submissionsXX"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_147() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["REAL_SUBMISSIONS"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_148() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(None)

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_149() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = None
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_150() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["XXstatusXX"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_151() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["STATUS"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_152() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] != "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_153() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "XXpendingXX"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_154() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "PENDING"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_155() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending or random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_156() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() <= 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_157() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 1.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_158() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = None
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_159() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(None)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_160() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = None
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_161() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["XXstatusXX"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_162() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["STATUS"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_163() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "XXcompletedXX"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_164() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "COMPLETED"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_165() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] = 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_166() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] -= 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_167() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["XXcompleted_tasksXX"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_168() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["COMPLETED_TASKS"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_169() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 2
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_170() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = None

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_171() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["XXqueue_lengthXX"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_172() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["QUEUE_LENGTH"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_173() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(None, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_174() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, None)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_175() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_176() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, )

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_177() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(1, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_178() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] + 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_179() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["XXqueue_lengthXX"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_180() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["QUEUE_LENGTH"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_181() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 2)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_182() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = None
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_183() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["XXstatusXX"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_184() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["STATUS"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_185() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] != "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_186() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "XXpendingXX"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_187() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "PENDING"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_188() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending or random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_189() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() <= 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_190() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 1.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_191() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = None
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_192() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(None)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_193() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = None

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_194() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["XXstatusXX"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_195() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["STATUS"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_196() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "XXrunningXX"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_197() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "RUNNING"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_198() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            None
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_199() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "XXtypeXX": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_200() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "TYPE": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_201() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "XXstatus_updateXX",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_202() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "STATUS_UPDATE",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_203() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "XXstatusXX": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_204() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "STATUS": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_205() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "XXtasksXX": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_206() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "TASKS": task_queue,
                "ppo_active": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_207() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "XXppo_activeXX": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_208() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "PPO_ACTIVE": _ppo_model is not None,
            }
        )


# ============================================================
# 后台模拟任务：定时更新状态（模拟调度引擎行为）
# ============================================================


async def x_simulate_scheduler__mutmut_209() -> None:
    """模拟调度引擎行为 — 使用 PPO 模型进行推理决策。

    每 3 秒推送一次状态更新。其中每 20 个 tick（约 60 秒）轮询一次天衍云
    真机状态（``query_quantum_computer_list``）和真机提交记录
    （``results/real_times.json``），将真实机器名/状态（running/calibrating/
    maintenance）与真实提交历史通过 WebSocket 推送到前端监控卡片。
    """
    import random

    tick = 0
    while True:
        await asyncio.sleep(3)
        tick += 1
        system_status["current_step"] += 1

        # 尝试使用 PPO 推理
        model = _get_ppo_model()
        if model is not None and model.env is not None and _ppo_env is not None:
            try:
                obs = model.env.reset()[0]
                action, _ = model.predict(obs, deterministic=True)
                # 根据 PPO 预测更新利用率
                target_qubit = 0.45 if action == 1 else (0.40 if action == 2 else 0.35)
                system_status["qubit_utilization"] = round(
                    system_status["qubit_utilization"] * 0.7 + target_qubit * 0.3, 4
                )
            except Exception:
                # PPO 推理失败，回退随机
                system_status["qubit_utilization"] = round(
                    max(
                        0.1,
                        min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03)),
                    ),
                    4,
                )
        else:
            # 无模型，随机模拟
            system_status["qubit_utilization"] = round(
                max(
                    0.1, min(1.0, system_status["qubit_utilization"] + random.uniform(-0.03, 0.03))
                ),
                4,
            )

        system_status["queue_length"] = len([t for t in task_queue if t["status"] == "pending"])
        system_status["average_wait_time"] = round(
            max(0.5, system_status["average_wait_time"] + random.uniform(-0.5, 0.5)), 1
        )
        system_status["last_update"] = datetime.now().isoformat()

        # 每 20 个 tick（约 60 秒）轮询真机状态 + 真机提交记录
        # 避免高频查询天衍云 API（免费额度有限）
        if tick % 20 == 0:
            try:
                real_machines = _get_real_machines_status()
                if real_machines:
                    system_status["real_machines"] = real_machines
            except Exception as e:
                print(f"[Web] 轮询真机状态异常: {e}")
            try:
                system_status["real_submissions"] = _load_real_submissions()
            except Exception as e:
                print(f"[Web] 加载真机提交记录异常: {e}")

        # PPO-Balanced 策略：平衡量子/经典资源分配
        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.35:
            task = random.choice(pending)
            task["status"] = "completed"
            system_status["completed_tasks"] += 1
            system_status["queue_length"] = max(0, system_status["queue_length"] - 1)

        pending = [t for t in task_queue if t["status"] == "pending"]
        if pending and random.random() < 0.25:
            task = random.choice(pending)
            task["status"] = "running"

        await manager.broadcast(
            {
                "type": "status_update",
                "status": system_status,
                "tasks": task_queue,
                "ppo_active": _ppo_model is None,
            }
        )

mutants_x_simulate_scheduler__mutmut['_mutmut_orig'] = x_simulate_scheduler__mutmut_orig # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_1'] = x_simulate_scheduler__mutmut_1 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_2'] = x_simulate_scheduler__mutmut_2 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_3'] = x_simulate_scheduler__mutmut_3 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_4'] = x_simulate_scheduler__mutmut_4 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_5'] = x_simulate_scheduler__mutmut_5 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_6'] = x_simulate_scheduler__mutmut_6 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_7'] = x_simulate_scheduler__mutmut_7 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_8'] = x_simulate_scheduler__mutmut_8 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_9'] = x_simulate_scheduler__mutmut_9 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_10'] = x_simulate_scheduler__mutmut_10 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_11'] = x_simulate_scheduler__mutmut_11 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_12'] = x_simulate_scheduler__mutmut_12 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_13'] = x_simulate_scheduler__mutmut_13 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_14'] = x_simulate_scheduler__mutmut_14 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_15'] = x_simulate_scheduler__mutmut_15 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_16'] = x_simulate_scheduler__mutmut_16 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_17'] = x_simulate_scheduler__mutmut_17 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_18'] = x_simulate_scheduler__mutmut_18 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_19'] = x_simulate_scheduler__mutmut_19 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_20'] = x_simulate_scheduler__mutmut_20 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_21'] = x_simulate_scheduler__mutmut_21 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_22'] = x_simulate_scheduler__mutmut_22 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_23'] = x_simulate_scheduler__mutmut_23 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_24'] = x_simulate_scheduler__mutmut_24 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_25'] = x_simulate_scheduler__mutmut_25 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_26'] = x_simulate_scheduler__mutmut_26 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_27'] = x_simulate_scheduler__mutmut_27 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_28'] = x_simulate_scheduler__mutmut_28 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_29'] = x_simulate_scheduler__mutmut_29 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_30'] = x_simulate_scheduler__mutmut_30 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_31'] = x_simulate_scheduler__mutmut_31 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_32'] = x_simulate_scheduler__mutmut_32 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_33'] = x_simulate_scheduler__mutmut_33 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_34'] = x_simulate_scheduler__mutmut_34 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_35'] = x_simulate_scheduler__mutmut_35 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_36'] = x_simulate_scheduler__mutmut_36 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_37'] = x_simulate_scheduler__mutmut_37 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_38'] = x_simulate_scheduler__mutmut_38 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_39'] = x_simulate_scheduler__mutmut_39 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_40'] = x_simulate_scheduler__mutmut_40 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_41'] = x_simulate_scheduler__mutmut_41 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_42'] = x_simulate_scheduler__mutmut_42 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_43'] = x_simulate_scheduler__mutmut_43 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_44'] = x_simulate_scheduler__mutmut_44 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_45'] = x_simulate_scheduler__mutmut_45 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_46'] = x_simulate_scheduler__mutmut_46 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_47'] = x_simulate_scheduler__mutmut_47 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_48'] = x_simulate_scheduler__mutmut_48 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_49'] = x_simulate_scheduler__mutmut_49 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_50'] = x_simulate_scheduler__mutmut_50 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_51'] = x_simulate_scheduler__mutmut_51 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_52'] = x_simulate_scheduler__mutmut_52 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_53'] = x_simulate_scheduler__mutmut_53 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_54'] = x_simulate_scheduler__mutmut_54 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_55'] = x_simulate_scheduler__mutmut_55 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_56'] = x_simulate_scheduler__mutmut_56 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_57'] = x_simulate_scheduler__mutmut_57 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_58'] = x_simulate_scheduler__mutmut_58 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_59'] = x_simulate_scheduler__mutmut_59 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_60'] = x_simulate_scheduler__mutmut_60 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_61'] = x_simulate_scheduler__mutmut_61 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_62'] = x_simulate_scheduler__mutmut_62 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_63'] = x_simulate_scheduler__mutmut_63 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_64'] = x_simulate_scheduler__mutmut_64 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_65'] = x_simulate_scheduler__mutmut_65 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_66'] = x_simulate_scheduler__mutmut_66 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_67'] = x_simulate_scheduler__mutmut_67 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_68'] = x_simulate_scheduler__mutmut_68 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_69'] = x_simulate_scheduler__mutmut_69 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_70'] = x_simulate_scheduler__mutmut_70 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_71'] = x_simulate_scheduler__mutmut_71 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_72'] = x_simulate_scheduler__mutmut_72 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_73'] = x_simulate_scheduler__mutmut_73 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_74'] = x_simulate_scheduler__mutmut_74 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_75'] = x_simulate_scheduler__mutmut_75 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_76'] = x_simulate_scheduler__mutmut_76 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_77'] = x_simulate_scheduler__mutmut_77 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_78'] = x_simulate_scheduler__mutmut_78 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_79'] = x_simulate_scheduler__mutmut_79 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_80'] = x_simulate_scheduler__mutmut_80 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_81'] = x_simulate_scheduler__mutmut_81 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_82'] = x_simulate_scheduler__mutmut_82 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_83'] = x_simulate_scheduler__mutmut_83 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_84'] = x_simulate_scheduler__mutmut_84 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_85'] = x_simulate_scheduler__mutmut_85 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_86'] = x_simulate_scheduler__mutmut_86 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_87'] = x_simulate_scheduler__mutmut_87 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_88'] = x_simulate_scheduler__mutmut_88 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_89'] = x_simulate_scheduler__mutmut_89 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_90'] = x_simulate_scheduler__mutmut_90 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_91'] = x_simulate_scheduler__mutmut_91 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_92'] = x_simulate_scheduler__mutmut_92 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_93'] = x_simulate_scheduler__mutmut_93 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_94'] = x_simulate_scheduler__mutmut_94 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_95'] = x_simulate_scheduler__mutmut_95 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_96'] = x_simulate_scheduler__mutmut_96 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_97'] = x_simulate_scheduler__mutmut_97 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_98'] = x_simulate_scheduler__mutmut_98 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_99'] = x_simulate_scheduler__mutmut_99 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_100'] = x_simulate_scheduler__mutmut_100 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_101'] = x_simulate_scheduler__mutmut_101 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_102'] = x_simulate_scheduler__mutmut_102 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_103'] = x_simulate_scheduler__mutmut_103 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_104'] = x_simulate_scheduler__mutmut_104 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_105'] = x_simulate_scheduler__mutmut_105 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_106'] = x_simulate_scheduler__mutmut_106 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_107'] = x_simulate_scheduler__mutmut_107 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_108'] = x_simulate_scheduler__mutmut_108 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_109'] = x_simulate_scheduler__mutmut_109 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_110'] = x_simulate_scheduler__mutmut_110 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_111'] = x_simulate_scheduler__mutmut_111 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_112'] = x_simulate_scheduler__mutmut_112 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_113'] = x_simulate_scheduler__mutmut_113 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_114'] = x_simulate_scheduler__mutmut_114 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_115'] = x_simulate_scheduler__mutmut_115 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_116'] = x_simulate_scheduler__mutmut_116 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_117'] = x_simulate_scheduler__mutmut_117 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_118'] = x_simulate_scheduler__mutmut_118 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_119'] = x_simulate_scheduler__mutmut_119 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_120'] = x_simulate_scheduler__mutmut_120 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_121'] = x_simulate_scheduler__mutmut_121 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_122'] = x_simulate_scheduler__mutmut_122 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_123'] = x_simulate_scheduler__mutmut_123 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_124'] = x_simulate_scheduler__mutmut_124 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_125'] = x_simulate_scheduler__mutmut_125 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_126'] = x_simulate_scheduler__mutmut_126 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_127'] = x_simulate_scheduler__mutmut_127 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_128'] = x_simulate_scheduler__mutmut_128 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_129'] = x_simulate_scheduler__mutmut_129 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_130'] = x_simulate_scheduler__mutmut_130 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_131'] = x_simulate_scheduler__mutmut_131 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_132'] = x_simulate_scheduler__mutmut_132 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_133'] = x_simulate_scheduler__mutmut_133 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_134'] = x_simulate_scheduler__mutmut_134 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_135'] = x_simulate_scheduler__mutmut_135 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_136'] = x_simulate_scheduler__mutmut_136 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_137'] = x_simulate_scheduler__mutmut_137 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_138'] = x_simulate_scheduler__mutmut_138 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_139'] = x_simulate_scheduler__mutmut_139 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_140'] = x_simulate_scheduler__mutmut_140 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_141'] = x_simulate_scheduler__mutmut_141 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_142'] = x_simulate_scheduler__mutmut_142 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_143'] = x_simulate_scheduler__mutmut_143 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_144'] = x_simulate_scheduler__mutmut_144 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_145'] = x_simulate_scheduler__mutmut_145 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_146'] = x_simulate_scheduler__mutmut_146 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_147'] = x_simulate_scheduler__mutmut_147 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_148'] = x_simulate_scheduler__mutmut_148 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_149'] = x_simulate_scheduler__mutmut_149 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_150'] = x_simulate_scheduler__mutmut_150 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_151'] = x_simulate_scheduler__mutmut_151 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_152'] = x_simulate_scheduler__mutmut_152 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_153'] = x_simulate_scheduler__mutmut_153 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_154'] = x_simulate_scheduler__mutmut_154 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_155'] = x_simulate_scheduler__mutmut_155 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_156'] = x_simulate_scheduler__mutmut_156 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_157'] = x_simulate_scheduler__mutmut_157 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_158'] = x_simulate_scheduler__mutmut_158 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_159'] = x_simulate_scheduler__mutmut_159 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_160'] = x_simulate_scheduler__mutmut_160 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_161'] = x_simulate_scheduler__mutmut_161 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_162'] = x_simulate_scheduler__mutmut_162 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_163'] = x_simulate_scheduler__mutmut_163 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_164'] = x_simulate_scheduler__mutmut_164 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_165'] = x_simulate_scheduler__mutmut_165 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_166'] = x_simulate_scheduler__mutmut_166 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_167'] = x_simulate_scheduler__mutmut_167 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_168'] = x_simulate_scheduler__mutmut_168 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_169'] = x_simulate_scheduler__mutmut_169 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_170'] = x_simulate_scheduler__mutmut_170 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_171'] = x_simulate_scheduler__mutmut_171 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_172'] = x_simulate_scheduler__mutmut_172 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_173'] = x_simulate_scheduler__mutmut_173 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_174'] = x_simulate_scheduler__mutmut_174 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_175'] = x_simulate_scheduler__mutmut_175 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_176'] = x_simulate_scheduler__mutmut_176 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_177'] = x_simulate_scheduler__mutmut_177 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_178'] = x_simulate_scheduler__mutmut_178 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_179'] = x_simulate_scheduler__mutmut_179 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_180'] = x_simulate_scheduler__mutmut_180 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_181'] = x_simulate_scheduler__mutmut_181 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_182'] = x_simulate_scheduler__mutmut_182 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_183'] = x_simulate_scheduler__mutmut_183 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_184'] = x_simulate_scheduler__mutmut_184 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_185'] = x_simulate_scheduler__mutmut_185 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_186'] = x_simulate_scheduler__mutmut_186 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_187'] = x_simulate_scheduler__mutmut_187 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_188'] = x_simulate_scheduler__mutmut_188 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_189'] = x_simulate_scheduler__mutmut_189 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_190'] = x_simulate_scheduler__mutmut_190 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_191'] = x_simulate_scheduler__mutmut_191 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_192'] = x_simulate_scheduler__mutmut_192 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_193'] = x_simulate_scheduler__mutmut_193 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_194'] = x_simulate_scheduler__mutmut_194 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_195'] = x_simulate_scheduler__mutmut_195 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_196'] = x_simulate_scheduler__mutmut_196 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_197'] = x_simulate_scheduler__mutmut_197 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_198'] = x_simulate_scheduler__mutmut_198 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_199'] = x_simulate_scheduler__mutmut_199 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_200'] = x_simulate_scheduler__mutmut_200 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_201'] = x_simulate_scheduler__mutmut_201 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_202'] = x_simulate_scheduler__mutmut_202 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_203'] = x_simulate_scheduler__mutmut_203 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_204'] = x_simulate_scheduler__mutmut_204 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_205'] = x_simulate_scheduler__mutmut_205 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_206'] = x_simulate_scheduler__mutmut_206 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_207'] = x_simulate_scheduler__mutmut_207 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_208'] = x_simulate_scheduler__mutmut_208 # type: ignore # mutmut generated
mutants_x_simulate_scheduler__mutmut['x_simulate_scheduler__mutmut_209'] = x_simulate_scheduler__mutmut_209 # type: ignore # mutmut generated


# ============================================================
# 前端 HTML 模板（原生 HTML/CSS/JS，不依赖前端框架）
# ============================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>量子RL调度系统 - 监控面板</title>
    <style>
        /* ===== 全局样式 ===== */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            min-height: 100vh;
        }

        /* ===== 顶部标题栏 ===== */
        .header {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-bottom: 1px solid #334155;
            padding: 16px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .header h1 {
            font-size: 22px;
            font-weight: 700;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header .ws-status {
            font-size: 13px;
            padding: 4px 12px;
            border-radius: 12px;
            background: #1e293b;
            border: 1px solid #334155;
        }
        .ws-status.connected { color: #4ade80; border-color: #22c55e; }
        .ws-status.disconnected { color: #f87171; border-color: #ef4444; }

        /* ===== 系统状态卡片区域 ===== */
        .status-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            padding: 24px 32px;
        }
        .status-card {
            background: linear-gradient(145deg, #1e293b, #1a2332);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 20px;
            transition: border-color 0.3s;
        }
        .status-card:hover { border-color: #60a5fa; }
        .status-card .card-label {
            font-size: 13px;
            color: #94a3b8;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .status-card .card-value {
            font-size: 32px;
            font-weight: 700;
            line-height: 1.2;
        }
        .status-card .card-sub {
            font-size: 12px;
            color: #64748b;
            margin-top: 6px;
        }
        /* 卡片颜色主题 */
        .card-blue .card-value { color: #60a5fa; }
        .card-purple .card-value { color: #a78bfa; }
        .card-green .card-value { color: #4ade80; }
        .card-amber .card-value { color: #fbbf24; }
        .card-cyan .card-value { color: #22d3ee; }

        /* ===== 主内容区域 ===== */
        .main-content {
            padding: 0 32px 32px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        /* ===== 通用面板样式 ===== */
        .panel {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            overflow: hidden;
        }
        .panel-header {
            padding: 14px 20px;
            border-bottom: 1px solid #334155;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .panel-header h2 {
            font-size: 16px;
            font-weight: 600;
        }
        .panel-header .badge {
            font-size: 12px;
            padding: 2px 10px;
            border-radius: 10px;
            background: #334155;
            color: #94a3b8;
        }
        .panel-body { padding: 16px 20px; }

        /* ===== 任务队列表格 ===== */
        .task-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        .task-table th {
            text-align: left;
            padding: 10px 12px;
            color: #94a3b8;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid #334155;
        }
        .task-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #1e293b;
        }
        .task-table tbody tr:hover { background: #253347; }
        .task-table tbody tr { transition: background 0.2s; }
        /* 状态标签 */
        .status-tag {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-tag.pending { background: rgba(251, 191, 36, 0.15); color: #fbbf24; }
        .status-tag.running { background: rgba(96, 165, 250, 0.15); color: #60a5fa; }
        .status-tag.completed { background: rgba(74, 222, 128, 0.15); color: #4ade80; }
        .status-tag.failed { background: rgba(248, 113, 113, 0.15); color: #f87171; }
        /* 优先级 */
        .priority-high { color: #f87171; }
        .priority-medium { color: #fbbf24; }
        .priority-low { color: #4ade80; }

        /* ===== 控制面板 ===== */
        .control-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .control-section h3 {
            font-size: 14px;
            color: #94a3b8;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        /* 表单样式 */
        .form-group {
            margin-bottom: 12px;
        }
        .form-group label {
            display: block;
            font-size: 13px;
            color: #94a3b8;
            margin-bottom: 4px;
        }
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 8px 12px;
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #e2e8f0;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }
        .form-group input:focus,
        .form-group select:focus {
            border-color: #60a5fa;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        /* 按钮 */
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #3b82f6, #6366f1);
            color: white;
        }
        .btn-primary:hover { opacity: 0.9; transform: translateY(-1px); }
        .btn-secondary {
            background: #334155;
            color: #e2e8f0;
        }
        .btn-secondary:hover { background: #475569; }
        .btn-secondary.active {
            background: linear-gradient(135deg, #3b82f6, #6366f1);
            color: white;
        }

        /* 策略选择按钮组 */
        .strategy-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .strategy-btn {
            padding: 8px 16px;
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #94a3b8;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .strategy-btn:hover { border-color: #60a5fa; color: #e2e8f0; }
        .strategy-btn.active {
            background: linear-gradient(135deg, #3b82f6, #6366f1);
            border-color: transparent;
            color: white;
        }

        /* ===== 通知 Toast ===== */
        .toast-container {
            position: fixed;
            top: 80px;
            right: 24px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .toast {
            padding: 12px 20px;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            font-size: 14px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            animation: slideIn 0.3s ease-out;
            max-width: 320px;
        }
        .toast.success { border-left: 3px solid #4ade80; }
        .toast.info { border-left: 3px solid #60a5fa; }
        .toast.warn { border-left: 3px solid #fbbf24; }
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        /* ===== 空状态 ===== */
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #64748b;
            font-size: 14px;
        }

        /* ===== 响应式 ===== */
        @media (max-width: 768px) {
            .header { padding: 12px 16px; }
            .header h1 { font-size: 16px; }
            .status-cards { padding: 16px; gap: 12px; }
            .main-content { padding: 0 16px 16px; }
            .control-grid { grid-template-columns: 1fr; }
            .form-row { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

    <!-- 顶部标题栏 -->
    <div class="header">
        <h1>量子RL调度系统 - 监控面板</h1>
        <span id="ws-status" class="ws-status disconnected">WebSocket 未连接</span>
    </div>

    <!-- 系统状态卡片 -->
    <div class="status-cards">
        <div class="status-card card-blue">
            <div class="card-label">量子比特利用率</div>
            <div class="card-value" id="val-qubit">0%</div>
            <div class="card-sub" id="sub-qubit">实时资源占用</div>
        </div>
        <div class="status-card card-purple">
            <div class="card-label">任务队列长度</div>
            <div class="card-value" id="val-queue">0</div>
            <div class="card-sub">等待调度执行</div>
        </div>
        <div class="status-card card-amber">
            <div class="card-label">平均等待时间</div>
            <div class="card-value" id="val-wait">0s</div>
            <div class="card-sub">最近100个任务</div>
        </div>
        <div class="status-card card-green">
            <div class="card-label">已完成任务</div>
            <div class="card-value" id="val-completed">0</div>
            <div class="card-sub">累计完成数</div>
        </div>
        <div class="status-card card-purple">
            <div class="card-label">PPO 排名</div>
            <div class="card-value" id="val-ppo-rank" style="font-size:28px;">-</div>
            <div class="card-sub" id="sub-ppo">8种策略对比</div>
        </div>
        <div class="status-card card-cyan">
            <div class="card-label">当前调度策略</div>
            <div class="card-value" id="val-strategy" style="font-size:20px;">-</div>
            <div class="card-sub" id="val-step">Step: 0</div>
        </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">

        <!-- 任务队列面板 -->
        <div class="panel">
            <div class="panel-header">
                <h2>任务队列</h2>
                <span class="badge" id="task-count">0 个任务</span>
            </div>
            <div class="panel-body" style="padding:0; overflow-x:auto;">
                <table class="task-table">
                    <thead>
                        <tr>
                            <th>任务ID</th>
                            <th>用户</th>
                            <th>类型</th>
                            <th>优先级</th>
                            <th>量子比特</th>
                            <th>预计时间</th>
                            <th>状态</th>
                            <th>到达时间</th>
                        </tr>
                    </thead>
                    <tbody id="task-tbody">
                        <!-- 由 JS 动态填充 -->
                    </tbody>
                </table>
                <div id="task-empty" class="empty-state" style="display:none;">
                    暂无任务，请在下方控制面板提交新任务
                </div>
            </div>
        </div>

        <!-- 控制面板 -->
        <div class="panel">
            <div class="panel-header">
                <h2>控制面板</h2>
            </div>
            <div class="panel-body">
                <div class="control-grid">

                    <!-- 左侧：提交新任务 -->
                    <div class="control-section">
                        <h3>提交新任务</h3>
                        <div class="form-group">
                            <label>用户ID</label>
                            <input type="text" id="input-user" value="user_001" placeholder="输入用户ID">
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>任务类型</label>
                                <select id="input-type">
                                    <option value="quantum">量子任务 (quantum)</option>
                                    <option value="classical">经典任务 (classical)</option>
                                    <option value="hybrid">混合任务 (hybrid)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>优先级 (1-5)</label>
                                <select id="input-priority">
                                    <option value="1">1 - 最低</option>
                                    <option value="2">2 - 低</option>
                                    <option value="3" selected>3 - 中</option>
                                    <option value="4">4 - 高</option>
                                    <option value="5">5 - 最高</option>
                                </select>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>量子比特数</label>
                                <input type="number" id="input-qubits" value="10" min="1">
                            </div>
                            <div class="form-group">
                                <label>电路深度</label>
                                <input type="number" id="input-depth" value="100" min="1">
                            </div>
                        </div>
                        <div class="form-group">
                            <label>预计执行时间(秒)</label>
                            <input type="number" id="input-time" value="60" min="0.1" step="0.1">
                        </div>
                        <button class="btn btn-primary" onclick="submitTask()" style="width:100%; margin-top:4px;">
                            提交任务
                        </button>
                    </div>

                    <!-- 右侧：调度策略切换 -->
                    <div class="control-section">
                        <h3>调度策略切换</h3>
                        <p style="font-size:13px; color:#64748b; margin-bottom:16px;">
                            选择当前使用的RL调度策略，切换后将立即生效。
                        </p>
                        <div class="strategy-buttons" id="strategy-buttons">
                            <!-- 由 JS 动态填充 -->
                        </div>
                    </div>

                </div>
            </div>
        </div>

    </div>

    <!-- Toast 通知容器 -->
    <div class="toast-container" id="toast-container"></div>

    <script>
        // ============================================================
        // 全局状态
        // ============================================================
        let ws = null;                // WebSocket 实例
        let currentStatus = {};       // 当前系统状态
        let currentTasks = [];       // 当前任务列表
        let reconnectTimer = null;   // 重连定时器
        let strategyOptions = [];     // 可用策略列表

        // ============================================================
        // 工具函数
        // ============================================================

        /** 显示 Toast 通知 */
        function showToast(message, type) {
            // type: 'success' | 'info' | 'warn'
            var container = document.getElementById('toast-container');
            var toast = document.createElement('div');
            toast.className = 'toast ' + type;
            toast.textContent = message;
            container.appendChild(toast);
            // 3秒后自动移除
            setTimeout(function() {
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            }, 3000);
        }

        /** 格式化时间字符串 */
        function formatTime(isoStr) {
            if (!isoStr) return '-';
            var d = new Date(isoStr);
            var hh = String(d.getHours()).padStart(2, '0');
            var mm = String(d.getMinutes()).padStart(2, '0');
            var ss = String(d.getSeconds()).padStart(2, '0');
            return hh + ':' + mm + ':' + ss;
        }

        /** 获取优先级样式 */
        function priorityClass(p) {
            if (p >= 4) return 'priority-high';
            if (p >= 3) return 'priority-medium';
            return 'priority-low';
        }

        /** 状态中文名 */
        function statusText(s) {
            var map = { pending: '等待中', running: '运行中', completed: '已完成', failed: '失败' };
            return map[s] || s;
        }

        // ============================================================
        // 页面渲染
        // ============================================================

        /** 更新顶部状态卡片 */
        function renderStatus(status, ppoStats) {
            document.getElementById('val-qubit').textContent =
                (status.qubit_utilization * 100).toFixed(1) + '%';
            document.getElementById('val-queue').textContent = status.queue_length;
            document.getElementById('val-wait').textContent = status.average_wait_time.toFixed(1) + 's';
            document.getElementById('val-completed').textContent = status.completed_tasks;
            document.getElementById('val-strategy').textContent = status.current_strategy || '-';
            document.getElementById('val-step').textContent = 'Step: ' + (status.current_step || 0);

            // PPO 排名
            if (ppoStats && ppoStats.ppo_rank) {
                var rankEl = document.getElementById('val-ppo-rank');
                rankEl.textContent = '#' + ppoStats.ppo_rank + ' / ' + (ppoStats.total || 8);
                var colors = ['#fbbf24', '#e2e8f0', '#cd7f32', '#94a3b8'];
                rankEl.style.color = colors[Math.min(ppoStats.ppo_rank - 1, 3)] || '#64748b';
                document.getElementById('sub-ppo').textContent = ppoStats.ppo_rank === 1 ? '🥇 策略对比第1名' : '8种策略对比';
            }
        }

        /** 更新任务队列表格 */
        function renderTasks(tasks) {
            var tbody = document.getElementById('task-tbody');
            var empty = document.getElementById('task-empty');
            var countBadge = document.getElementById('task-count');

            countBadge.textContent = tasks.length + ' 个任务';

            if (tasks.length === 0) {
                tbody.innerHTML = '';
                empty.style.display = 'block';
                return;
            }
            empty.style.display = 'none';

            // 按优先级降序、到达时间升序排列
            var sorted = tasks.slice().sort(function(a, b) {
                if (a.status === 'pending' && b.status !== 'pending') return -1;
                if (a.status !== 'pending' && b.status === 'pending') return 1;
                return b.priority - a.priority;
            });

            var html = '';
            for (var i = 0; i < sorted.length; i++) {
                var t = sorted[i];
                html += '<tr>' +
                    '<td style="font-family:monospace;color:#94a3b8;">' + t.task_id + '</td>' +
                    '<td>' + t.user_id + '</td>' +
                    '<td>' + t.task_type + '</td>' +
                    '<td><span class="' + priorityClass(t.priority) + '">' + t.priority + '</span></td>' +
                    '<td>' + (t.qubit_count || '-') + '</td>' +
                    '<td>' + (t.estimated_time || '-') + 's</td>' +
                    '<td><span class="status-tag ' + t.status + '">' + statusText(t.status) + '</span></td>' +
                    '<td style="color:#64748b;">' + formatTime(t.arrival_time) + '</td>' +
                    '</tr>';
            }
            tbody.innerHTML = html;
        }

        /** 渲染策略选择按钮 */
        function renderStrategies(strategies, currentStrategy) {
            var container = document.getElementById('strategy-buttons');
            var html = '';
            for (var i = 0; i < strategies.length; i++) {
                var s = strategies[i];
                var activeClass = (s === currentStrategy) ? ' active' : '';
                html += '<button class="strategy-btn' + activeClass + '" ' +
                    'onclick="switchStrategy(\\'' + s + '\\')">' + s + '</button>';
            }
            container.innerHTML = html;
        }

        // ============================================================
        // API 调用
        // ============================================================

        /** 初始加载：拉取系统状态和任务列表 */
        async function fetchInitialState() {
            try {
                var statusResp = await fetch('/api/status');
                currentStatus = await statusResp.json();

                var tasksResp = await fetch('/api/tasks');
                currentTasks = await tasksResp.json();

                strategyOptions = currentStatus.strategy_options || [];

                // 拉取 PPO 统计数据
                var ppoStats = {};
                try {
                    var ppoResp = await fetch('/api/ppo/stats');
                    var ppoData = await ppoResp.json();
                    if (ppoData.ppo_rank) {
                        ppoStats = { ppo_rank: ppoData.ppo_rank, total: ppoData.total };
                    }
                } catch (e) { /* 忽略 PPO 加载失败 */ }

                renderStatus(currentStatus, ppoStats);
                renderTasks(currentTasks);
                renderStrategies(strategyOptions, currentStatus.current_strategy);
            } catch (e) {
                console.error('初始数据加载失败:', e);
            }
        }

        /** 提交新任务 */
        async function submitTask() {
            var payload = {
                user_id: document.getElementById('input-user').value || 'user_001',
                task_type: document.getElementById('input-type').value,
                priority: parseInt(document.getElementById('input-priority').value),
                qubit_count: parseInt(document.getElementById('input-qubits').value) || 10,
                circuit_depth: parseInt(document.getElementById('input-depth').value) || 100,
                estimated_time: parseFloat(document.getElementById('input-time').value) || 60.0,
            };
            try {
                var resp = await fetch('/api/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
                var result = await resp.json();
                if (result.task_id) {
                    showToast('任务已提交: ' + result.task_id, 'success');
                } else {
                    showToast('提交结果: ' + result.message, 'info');
                }
            } catch (e) {
                showToast('提交失败: ' + e.message, 'warn');
            }
        }

        /** 切换调度策略 */
        async function switchStrategy(strategy) {
            try {
                var resp = await fetch('/api/strategy?strategy=' + encodeURIComponent(strategy), {
                    method: 'POST',
                });
                var result = await resp.json();
                if (result.success) {
                    showToast(result.message, 'success');
                } else {
                    showToast(result.message, 'warn');
                }
            } catch (e) {
                showToast('策略切换失败: ' + e.message, 'warn');
            }
        }

        // ============================================================
        // WebSocket 连接管理
        // ============================================================

        function connectWebSocket() {
            var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            var wsUrl = protocol + '//' + window.location.host + '/ws';
            ws = new WebSocket(wsUrl);

            // 更新连接状态指示器
            var statusEl = document.getElementById('ws-status');

            ws.onopen = function() {
                statusEl.textContent = 'WebSocket 已连接';
                statusEl.className = 'ws-status connected';
                console.log('WebSocket 已连接');
                // 清除重连定时器
                if (reconnectTimer) {
                    clearTimeout(reconnectTimer);
                    reconnectTimer = null;
                }
            };

            ws.onmessage = function(event) {
                var msg = JSON.parse(event.data);

                if (msg.type === 'init') {
                    // 初始化消息：包含当前状态和任务
                    currentStatus = msg.status;
                    currentTasks = msg.tasks || [];
                    strategyOptions = currentStatus.strategy_options || [];
                    renderStatus(currentStatus, msg.ppo_stats);
                    renderTasks(currentTasks);
                    renderStrategies(strategyOptions, currentStatus.current_strategy);

                } else if (msg.type === 'status_update') {
                    // 状态更新
                    if (msg.status) {
                        currentStatus = msg.status;
                        renderStatus(currentStatus);
                    }
                    if (msg.tasks) {
                        currentTasks = msg.tasks;
                        renderTasks(currentTasks);
                    }

                } else if (msg.type === 'task_added') {
                    // 新任务通知
                    if (msg.status) {
                        currentStatus = msg.status;
                        renderStatus(currentStatus);
                    }
                    // 拉取最新任务列表
                    fetch('/api/tasks').then(function(r) {
                        return r.json();
                    }).then(function(tasks) {
                        currentTasks = tasks;
                        renderTasks(currentTasks);
                    });

                } else if (msg.type === 'strategy_changed') {
                    // 策略变更通知
                    if (msg.status) {
                        currentStatus = msg.status;
                        renderStatus(currentStatus);
                        renderStrategies(
                            currentStatus.strategy_options || strategyOptions,
                            currentStatus.current_strategy
                        );
                    }
                    showToast('策略已切换: ' + msg.new_strategy, 'info');

                } else if (msg.type === 'pong') {
                    // 心跳响应，无需处理
                }
            };

            ws.onclose = function() {
                statusEl.textContent = 'WebSocket 已断开';
                statusEl.className = 'ws-status disconnected';
                console.log('WebSocket 已断开，3秒后尝试重连...');
                // 自动重连
                reconnectTimer = setTimeout(function() {
                    connectWebSocket();
                }, 3000);
            };

            ws.onerror = function(err) {
                console.error('WebSocket 错误:', err);
                ws.close();
            };

            // 心跳：每30秒发送一次 ping
            setInterval(function() {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ action: 'ping' }));
                }
            }, 30000);
        }

        // ============================================================
        // 页面初始化
        // ============================================================

        (function init() {
            // 先加载初始数据（HTTP 方式）
            fetchInitialState();
            // 然后建立 WebSocket 连接（实时更新）
            connectWebSocket();
        })();
    </script>
</body>
</html>"""
mutants_x_start_web_server__mutmut: MutantDict = {}  # type: ignore


# ============================================================
# 服务器启动入口
# ============================================================


@_mutmut_mutated(mutants_x_start_web_server__mutmut)
def start_web_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_orig(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_1(host: str = "XX0.0.0.0XX", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_2(host: str = "0.0.0.0", port: int = 8001) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_3(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print(None)
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_4(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("XX========================================XX")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_5(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print(None)
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_6(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("XX  量子RL调度系统 - 监控面板XX")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_7(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子rl调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_8(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(None)
    print("========================================")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_9(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print(None)
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_10(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("XX========================================XX")
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_11(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(None, host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_12(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=None, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_13(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, port=None)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_14(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(host=host, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_15(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, port=port)


# ============================================================
# 服务器启动入口
# ============================================================


def x_start_web_server__mutmut_16(host: str = "0.0.0.0", port: int = 8000) -> None:
    """启动 Web 服务器"""
    import uvicorn

    print("========================================")
    print("  量子RL调度系统 - 监控面板")
    print(f"  访问地址: http://{host}:{port}")
    print("========================================")
    uvicorn.run(app, host=host, )

mutants_x_start_web_server__mutmut['_mutmut_orig'] = x_start_web_server__mutmut_orig # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_1'] = x_start_web_server__mutmut_1 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_2'] = x_start_web_server__mutmut_2 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_3'] = x_start_web_server__mutmut_3 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_4'] = x_start_web_server__mutmut_4 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_5'] = x_start_web_server__mutmut_5 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_6'] = x_start_web_server__mutmut_6 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_7'] = x_start_web_server__mutmut_7 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_8'] = x_start_web_server__mutmut_8 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_9'] = x_start_web_server__mutmut_9 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_10'] = x_start_web_server__mutmut_10 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_11'] = x_start_web_server__mutmut_11 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_12'] = x_start_web_server__mutmut_12 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_13'] = x_start_web_server__mutmut_13 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_14'] = x_start_web_server__mutmut_14 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_15'] = x_start_web_server__mutmut_15 # type: ignore # mutmut generated
mutants_x_start_web_server__mutmut['x_start_web_server__mutmut_16'] = x_start_web_server__mutmut_16 # type: ignore # mutmut generated


if __name__ == "__main__":
    start_web_server()
