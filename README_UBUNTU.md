# 大语言模型演示项目 - Ubuntu 22.04 部署版

## 🚀 快速开始

这是专门为 Ubuntu 22.04 + Python 3.10 环境优化的部署分支。

### 一键部署

```bash
# 1. 克隆项目并切换到部署分支
git clone <your-repo-url>
cd llm-exp
git checkout deploy-ubuntu

# 2. 运行自动部署脚本
./deploy_ubuntu.sh

# 3. 启动应用
./start_app.sh
```

### 访问应用

在浏览器中打开：http://localhost:8501

## 📋 系统要求

- **操作系统**: Ubuntu 22.04 LTS
- **Python**: 3.10.x
- **内存**: 最少 4GB（推荐 8GB+）
- **存储**: 最少 10GB 可用空间
- **网络**: 稳定的互联网连接

## 📁 部署文件说明

### 核心部署文件

- `deploy_ubuntu.sh` - 自动部署脚本
- `start_app.sh` - 应用启动脚本（由部署脚本生成）
- `requirements_lin.txt` - Ubuntu优化的Python依赖
- `.env.ubuntu` - 环境变量配置

### Docker部署文件

- `Dockerfile.ubuntu` - Ubuntu Docker镜像配置
- `docker-compose.ubuntu.yml` - Docker Compose配置

### 文档文件

- `DEPLOY_UBUNTU.md` - 详细部署指南
- `SYSTEM_REQUIREMENTS.md` - 系统依赖安装指南
- `README_UBUNTU.md` - 本文件

## 🐳 Docker 部署

### 使用 Docker Compose

```bash
docker-compose -f docker-compose.ubuntu.yml up -d
```

### 使用 Docker

```bash
# 构建镜像
docker build -f Dockerfile.ubuntu -t llm-demo:ubuntu .

# 运行容器
docker run -d --name llm-demo-ubuntu -p 8501:8501 llm-demo:ubuntu
```

## 🔧 手动部署

如果自动脚本无法使用，请参考 [DEPLOY_UBUNTU.md](DEPLOY_UBUNTU.md) 进行手动部署。

## 📦 依赖包优化

本分支对 `requirements_lin.txt` 进行了以下优化：

- **PyTorch**: 降级到 2.5.1（更稳定）
- **Transformers**: 降级到 4.46.3（兼容性更好）
- **Streamlit**: 降级到 1.39.0（稳定版本）
- **NumPy**: 使用 1.24.4（Python 3.10兼容）
- **其他包**: 选择了在Ubuntu 22.04上测试过的稳定版本

## 🎯 功能特性

- **中文模型**: Qwen2-1.5B
- **英文模型**: GPT-2
- **交互式界面**: 基于Streamlit
- **实时预测**: 下一个词元预测
- **参数调节**: 温度、Top-K采样
- **自动/手动模式**: 灵活的生成方式

## 🛠️ 故障排除

### 常见问题

1. **模型下载慢**
   ```bash
   export HF_ENDPOINT=https://hf-mirror.com
   ```

2. **内存不足**
   ```bash
   export OMP_NUM_THREADS=2
   export MKL_NUM_THREADS=2
   ```

3. **端口占用**
   ```bash
   # 使用其他端口
   streamlit run Home.py --server.port=8502
   ```

### 获取帮助

- 查看详细部署指南：[DEPLOY_UBUNTU.md](DEPLOY_UBUNTU.md)
- 查看系统要求：[SYSTEM_REQUIREMENTS.md](SYSTEM_REQUIREMENTS.md)
- 提交Issue到项目仓库

## 📝 更新日志

### v1.0.0 (deploy-ubuntu分支)

- ✅ 创建Ubuntu 22.04专用部署分支
- ✅ 优化Python依赖包版本
- ✅ 添加自动部署脚本
- ✅ 提供Docker部署选项
- ✅ 完善部署文档

## 🤝 贡献

欢迎提交Issue和Pull Request来改进Ubuntu部署体验。

## 📄 许可证

本项目遵循原项目的许可证。

---

**注意**: 首次运行需要下载模型文件（约2-3GB），请保持网络连接稳定。
