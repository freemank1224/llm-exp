# 📋 GitHub 镜像发布指南

本指南帮助您将Docker镜像发布到GitHub Container Registry (GHCR)，让其他用户可以直接使用您的预构建镜像。

## 🔧 准备工作

### 1. 创建GitHub Personal Access Token

1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token (classic)"
3. 设置token名称，例如：`docker-ghcr-token`
4. 选择以下权限：
   - ✅ `write:packages` - 上传包到GitHub Package Registry
   - ✅ `read:packages` - 从GitHub Package Registry下载包
   - ✅ `delete:packages` - 删除GitHub Package Registry中的包
5. 点击 "Generate token" 并**立即复制保存**（只显示一次）

### 2. 配置本地环境

```bash
# 设置环境变量（可选，或直接输入到命令中）
export GITHUB_USERNAME="your-github-username"
export GITHUB_TOKEN="your_personal_access_token"
```

## 🚀 发布方法

### 方法一：使用自动化脚本（推荐）

1. **编辑推送脚本**：
   ```bash
   # 编辑 push_docker.sh，设置您的GitHub用户名
   nano push_docker.sh
   # 修改这一行：GITHUB_USERNAME="your-github-username"
   ```

2. **运行推送脚本**：
   ```bash
   ./push_docker.sh
   ```

### 方法二：手动命令行

1. **登录到GHCR**：
   ```bash
   echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin
   # 或者交互式登录
   docker login ghcr.io -u your-github-username
   ```

2. **标记镜像**：
   ```bash
   # 将本地镜像标记为远程镜像
   docker tag llm-prediction-app:latest ghcr.io/your-github-username/llm-exp:latest
   
   # 可选：添加版本标签
   docker tag llm-prediction-app:latest ghcr.io/your-github-username/llm-exp:v1.0.0
   ```

3. **推送镜像**：
   ```bash
   # 推送latest标签
   docker push ghcr.io/your-github-username/llm-exp:latest
   
   # 推送版本标签
   docker push ghcr.io/your-github-username/llm-exp:v1.0.0
   ```

### 方法三：使用GitHub Actions（自动化）

我们已经为您准备了GitHub Actions工作流文件 `.github/workflows/docker-build-push.yml`。

1. **推送代码到GitHub**：
   ```bash
   git add .
   git commit -m "Add Docker build and push workflow"
   git push origin main
   ```

2. **GitHub Actions将自动**：
   - 构建Docker镜像
   - 推送到GHCR
   - 为每个tag创建版本化镜像

## 📦 验证发布

### 检查GHCR中的镜像

1. 访问您的GitHub仓库
2. 点击右侧的 "Packages" 链接
3. 您应该能看到 `llm-exp` 包

### 测试拉取镜像

```bash
# 拉取镜像
docker pull ghcr.io/your-github-username/llm-exp:latest

# 运行测试
docker run -d -p 8501:8501 ghcr.io/your-github-username/llm-exp:latest
```

## 🔒 设置镜像可见性

### 设为公开（推荐用于开源项目）

1. 访问 GitHub → 您的仓库 → Packages
2. 点击包名称进入包页面
3. 点击 "Package settings"
4. 在 "Danger Zone" 中点击 "Change visibility"
5. 选择 "Public" 并确认

### 设为私有

保持默认设置，只有您和协作者可以访问。

## 📝 更新文档

发布成功后，更新以下文件中的镜像地址：

### 1. README.md
```markdown
# 替换 YOUR-USERNAME 为您的实际GitHub用户名
docker pull ghcr.io/YOUR-USERNAME/llm-exp:latest
```

### 2. DOCKER_USAGE.md
同样替换所有的 `YOUR-USERNAME`。

### 3. 创建Release说明
在GitHub仓库中创建Release，说明：
- Docker镜像版本
- 包含的模型版本
- 更新内容
- 使用说明

## 🐛 常见问题解决

### 问题1: `permission_denied: create_package`
**原因**: Personal Access Token权限不足
**解决**: 确保token有 `write:packages` 权限

### 问题2: `authentication required`
**原因**: 未正确登录GHCR
**解决**: 
```bash
docker logout ghcr.io
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin
```

### 问题3: `requested access to the resource is denied`
**原因**: 用户名或仓库名不匹配
**解决**: 确保镜像标签中的用户名与GitHub用户名一致

### 问题4: 推送速度慢
**原因**: 镜像较大（约3GB+）
**解决**: 
- 使用稳定网络连接
- 考虑分层推送
- 使用GitHub Actions在云端构建

## 📊 镜像管理

### 查看镜像大小
```bash
docker images ghcr.io/your-github-username/llm-exp
```

### 删除本地标签
```bash
docker rmi ghcr.io/your-github-username/llm-exp:latest
```

### 删除远程镜像
在GitHub Package页面的设置中删除。

## 🔄 版本管理建议

### 语义化版本
- `v1.0.0` - 主要版本
- `v1.0.1` - 补丁版本
- `latest` - 最新稳定版

### 标签策略
```bash
# 为每个发布版本创建标签
docker tag llm-prediction-app:latest ghcr.io/username/llm-exp:v1.0.0
docker tag llm-prediction-app:latest ghcr.io/username/llm-exp:latest

# 推送所有标签
docker push ghcr.io/username/llm-exp:v1.0.0
docker push ghcr.io/username/llm-exp:latest
```

---

完成这些步骤后，您的Docker镜像将可供全世界的用户使用！🌍
