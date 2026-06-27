# Docker 部署说明

## 快速开始

### 1. 构建并启动服务

```bash
# 构建镜像
docker build -t quantum-rl-scheduler:latest .

# 启动服务
docker-compose up -d
```

### 2. 访问服务

- **Web 监控界面**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **TensorBoard** (可选): http://localhost:6006

```bash
# 启动包含 TensorBoard 的完整服务
docker-compose --profile monitoring up -d
```

## 常用命令

```bash
# 查看日志
docker-compose logs -f web

# 停止服务
docker-compose down

# 重新构建并启动
docker-compose up -d --build

# 进入容器
docker exec -it quantum-rl-web bash

# 查看容器状态
docker-compose ps
```

## 数据持久化

日志和模型文件会持久化到宿主机的 `logs/` 和 `models/` 目录。

```bash
# 查看训练日志
ls -la logs/

# 查看保存的模型
ls -la models/
```

## 生产环境部署

对于生产环境，建议：

1. 启动 Redis 缓存：
```bash
docker-compose --profile production up -d
```

2. 配置环境变量：
```bash
# 创建 .env 文件
echo "LOG_LEVEL=INFO" > .env
echo "REDIS_URL=redis://redis:6379" >> .env
```

3. 使用 Nginx 反向代理

## GPU 支持（可选）

如果需要在 Docker 中使用 GPU：

```bash
# NVIDIA GPU
docker build -t quantum-rl-scheduler:latest . \
  --build-arg CUDA_VERSION=11.8

# 运行带 GPU 支持的容器
docker run --gpus all -p 8000:8000 quantum-rl-scheduler:latest
```

## 故障排除

### 端口被占用
```bash
# 查看端口占用
netstat -tulpn | grep 8000

# 修改 docker-compose.yml 中的端口映射
```

### 内存不足
```bash
# 增加 Docker 内存限制
# Docker Desktop -> Settings -> Resources -> Memory
```

### 构建失败
```bash
# 清理 Docker 缓存
docker builder prune -a

# 重新构建
docker-compose build --no-cache
```
