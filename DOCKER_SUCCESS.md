# 🐳 Docker镜像发布成功！

## 📦 镜像信息

- **镜像地址**: `ghcr.io/freemank1224/llm-exp:latest`
- **镜像大小**: 约 3GB（包含预下载的Qwen2-1.5B模型）
- **GitHub包页面**: https://github.com/freemank1224/llm-exp/pkgs/container/llm-exp

## 🚀 一键体验

### 方法一：直接运行
```bash
docker run -d -p 8501:8501 --name llm-prediction ghcr.io/freemank1224/llm-exp:latest
```

### 方法二：使用快速部署脚本
```bash
curl -sSL https://raw.githubusercontent.com/freemank1224/llm-exp/main/quick_deploy.sh | bash
```

### 方法三：使用Docker Compose
```bash
# 下载配置文件
curl -O https://raw.githubusercontent.com/freemank1224/llm-exp/main/docker-compose.yml

# 启动服务
docker-compose up -d
```

## 🌐 访问应用

启动成功后，在浏览器中访问：http://localhost:8501

## 📋 管理命令

```bash
# 查看容器状态
docker ps

# 查看日志
docker logs llm-prediction

# 停止容器
docker stop llm-prediction

# 重启容器
docker restart llm-prediction

# 删除容器
docker rm llm-prediction

# 删除镜像
docker rmi ghcr.io/freemank1224/llm-exp:latest
```

## 🎯 应用特点

- ✅ **零配置运行**: 无需安装Python环境
- ✅ **模型预装**: Qwen2-1.5B模型已内置，启动即用
- ✅ **跨平台**: 支持Windows/macOS/Linux
- ✅ **中英双语**: 支持中英文文本预测
- ✅ **教育友好**: 专为LLM教学设计

## 📊 系统要求

- Docker Desktop 或 Docker Engine
- 最少 4GB 可用内存
- 最少 5GB 可用磁盘空间
- 网络连接（首次拉取镜像）

## 🔗 相关链接

- **GitHub仓库**: https://github.com/freemank1224/llm-exp
- **Docker镜像**: https://github.com/freemank1224/llm-exp/pkgs/container/llm-exp
- **使用文档**: https://github.com/freemank1224/llm-exp/blob/main/DOCKER_USAGE.md

---

🎉 **恭喜！您的LLM预测应用现在可以被全世界的用户一键使用了！**
