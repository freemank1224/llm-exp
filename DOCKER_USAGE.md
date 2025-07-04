# 🐳 Docker 部署使用指南

本项目提供了完整的Docker解决方案，让您无需配置复杂的Python环境即可运行LLM预测应用。

## 🎯 快速开始

### 方式一：使用预构建镜像（推荐）

我们已经为您构建好了包含所有依赖和模型的Docker镜像，您只需一条命令即可运行：

```bash
# 拉取并运行镜像
docker run -d -p 8501:8501 --name llm-prediction ghcr.io/YOUR-USERNAME/llm-exp:latest

# 访问应用
open http://localhost:8501
```

### 方式二：本地构建镜像

如果您想自己构建镜像或者需要修改代码：

```bash
# 1. 克隆项目
git clone https://github.com/YOUR-USERNAME/llm-exp.git
cd llm-exp

# 2. 构建镜像（自动化脚本）
./build_docker.sh

# 3. 运行容器（自动化脚本）
./run_docker.sh
```

## 📋 详细使用说明

### 系统要求

- Docker Desktop (Windows/macOS) 或 Docker Engine (Linux)
- 至少 8GB 可用磁盘空间
- 至少 4GB 可用内存

### 端口配置

- 默认端口：`8501`
- 访问地址：`http://localhost:8501`
- 自定义端口：`docker run -p YOUR_PORT:8501 ...`

### 容器管理命令

```bash
# 查看运行状态
docker ps

# 查看日志
docker logs llm-prediction

# 实时查看日志
docker logs -f llm-prediction

# 停止容器
docker stop llm-prediction

# 重启容器
docker restart llm-prediction

# 删除容器
docker rm llm-prediction

# 删除镜像
docker rmi ghcr.io/YOUR-USERNAME/llm-exp:latest
```

## 🔧 高级配置

### 环境变量

您可以通过环境变量自定义配置：

```bash
docker run -d \
  -p 8501:8501 \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  --name llm-prediction \
  ghcr.io/YOUR-USERNAME/llm-exp:latest
```

### 数据持久化

如果您需要持久化某些数据：

```bash
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  --name llm-prediction \
  ghcr.io/YOUR-USERNAME/llm-exp:latest
```

### 资源限制

为容器设置资源限制：

```bash
docker run -d \
  -p 8501:8501 \
  --memory=4g \
  --cpus=2 \
  --name llm-prediction \
  ghcr.io/YOUR-USERNAME/llm-exp:latest
```

## 🚀 生产部署

### 使用 Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'
services:
  llm-prediction:
    image: ghcr.io/YOUR-USERNAME/llm-exp:latest
    ports:
      - "8501:8501"
    restart: unless-stopped
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2'
```

运行：
```bash
docker-compose up -d
```

### 反向代理配置

如果您使用 Nginx 作为反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## ❓ 常见问题

### Q: 镜像太大怎么办？
A: 我们的镜像包含了完整的LLM模型（约3GB），这是为了确保离线运行。如果存储空间有限，可以考虑使用较小的模型版本。

### Q: 容器启动失败？
A: 请检查：
1. Docker是否正常运行
2. 端口8501是否被占用
3. 系统内存是否充足（建议4GB+）

### Q: 如何更新到最新版本？
A: 
```bash
# 停止并删除旧容器
docker stop llm-prediction && docker rm llm-prediction

# 拉取最新镜像
docker pull ghcr.io/YOUR-USERNAME/llm-exp:latest

# 运行新容器
docker run -d -p 8501:8501 --name llm-prediction ghcr.io/YOUR-USERNAME/llm-exp:latest
```

### Q: 如何查看容器内部？
A: 
```bash
# 进入容器shell
docker exec -it llm-prediction /bin/bash

# 查看文件
docker exec llm-prediction ls -la /app
```

## 🛠️ 开发者信息

### 构建信息
- 基础镜像：`python:3.10-slim`
- 模型：Qwen2-1.5B
- 框架：Streamlit
- 缓存目录：`/app/models`

### 自定义构建
如果您需要修改模型或配置，可以编辑以下文件：
- `Dockerfile`：镜像构建配置
- `download_models.py`：模型下载脚本
- `requirements.txt`：Python依赖

## 📞 支持

如果您在使用Docker部署时遇到问题：

1. 查看项目 [Issues](https://github.com/YOUR-USERNAME/llm-exp/issues)
2. 提交新的 Issue 并包含：
   - 操作系统信息
   - Docker版本
   - 错误日志
   - 重现步骤

---

更多详细信息请参考项目主 [README.md](README.md)。
