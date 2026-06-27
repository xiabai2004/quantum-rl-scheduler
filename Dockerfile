# =============================================================================
# 量子RL调度系统 - Docker 镜像构建文件
# Quantum RL Scheduler - Docker Image Build File
#
# 使用多阶段构建优化镜像大小：
#   - 阶段1：安装依赖（构建依赖）
#   - 阶段2：运行时环境（精简镜像）
#
# 构建镜像：
#   docker build -t quantum-rl-scheduler:latest .
#
# 运行容器：
#   docker run -p 8000:8000 -p 6006:6006 quantum-rl-scheduler:latest
#
# 使用 docker-compose（推荐）：
#   docker-compose up -d
# =============================================================================

# -----------------------------------------------------------------------------
# 阶段1：依赖安装
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS builder

# 设置工作目录
WORKDIR /app

# 安装构建工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖（使用 pip 的缓存机制）
RUN pip install --no-cache-dir --user -r requirements.txt

# -----------------------------------------------------------------------------
# 阶段2：运行时环境
# -----------------------------------------------------------------------------
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装运行时依赖（不需要编译的包）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 从构建阶段复制已安装的 Python 包
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 复制项目代码
COPY . .

# 创建必要的目录
RUN mkdir -p logs models

# 暴露端口
# 8000: FastAPI Web 服务
# 6006: TensorBoard（可选）
EXPOSE 8000 6006

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/status || exit 1

# 默认启动命令：启动 Web 服务
CMD ["python", "-m", "uvicorn", "src.visualization.app:app", "--host", "0.0.0.0", "--port", "8000"]

# 备用启动命令（用于扩展）：
# - 训练模式: python scripts/train_agent.py --timesteps 100000
# - 快速训练: python scripts/quick_train.py
