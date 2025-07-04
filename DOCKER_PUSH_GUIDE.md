# 🚀 Docker 推送快速指南

## 问题：无法粘贴 GitHub Token？

如果您在运行 `./push_docker.sh` 时无法粘贴 GitHub Personal Access Token，请尝试以下解决方案：

### 方案一：使用专用登录脚本（推荐）

```bash
# 1. 先运行登录脚本
./login_docker.sh

# 2. 登录成功后再推送
./push_docker.sh
```

### 方案二：使用环境变量

```bash
# 1. 设置环境变量（将 YOUR_TOKEN 替换为实际的token）
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# 2. 运行推送脚本
./push_docker.sh
```

### 方案三：手动登录Docker

```bash
# 1. 手动登录（会提示输入密码，此时可以粘贴token）
docker login ghcr.io -u freemank1224

# 2. 运行推送脚本
./push_docker.sh
```

### 方案四：一条命令登录

```bash
# 直接运行（将 YOUR_TOKEN 替换为实际的token）
echo "ghp_xxxxxxxxxxxxxxxxxxxx" | docker login ghcr.io -u freemank1224 --password-stdin
```

## 获取 GitHub Personal Access Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 设置名称：`docker-ghcr-token`
4. 选择权限：
   - ✅ `write:packages`
   - ✅ `read:packages`
   - ✅ `delete:packages`
5. 点击 "Generate token"
6. **立即复制保存**（只显示一次！）

## 验证登录状态

```bash
# 检查是否已登录
docker system info | grep Username

# 或者尝试拉取一个私有镜像
docker pull ghcr.io/freemank1224/test:latest
```

## 完整推送流程

```bash
# 1. 构建镜像
./build_docker.sh

# 2. 登录GHCR（选择最适合的方法）
./login_docker.sh

# 3. 推送镜像
./push_docker.sh
```

## 常见问题

### Q: 提示 "permission_denied"
A: Token权限不足，确保有 `write:packages` 权限

### Q: 提示 "authentication required"
A: 未正确登录，重新运行登录步骤

### Q: 无法粘贴密码
A: 使用上述任意一种替代方案

### Q: 推送速度慢
A: 镜像较大（3GB+），需要稳定网络连接，请耐心等待

---

💡 **推荐使用 `./login_docker.sh` 脚本，它提供了多种登录方式，总有一种适合您！**
