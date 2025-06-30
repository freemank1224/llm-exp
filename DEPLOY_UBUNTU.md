# Ubuntu 22.04 部署指南

## 项目简介

这是一个大语言模型演示项目，展示了GPT-2和Qwen2-1.5B模型的下一个词元预测功能。项目基于Streamlit构建，提供了直观的Web界面。

## 快速部署

### 方法一：自动部署脚本（推荐）

1. **克隆项目并切换到部署分支**
   ```bash
   git clone <your-repo-url>
   cd llm-exp
   git checkout deploy-ubuntu
   ```

2. **运行自动部署脚本**
   ```bash
   ./deploy_ubuntu.sh
   ```

3. **启动应用**
   ```bash
   ./start_app.sh
   ```

4. **访问应用**
   
   在浏览器中打开：http://localhost:8501

### 方法二：手动部署

#### 步骤1：系统环境准备

1. **检查系统版本**
   ```bash
   lsb_release -a
   # 确保是Ubuntu 22.04
   ```

2. **检查Python版本**
   ```bash
   python3 --version
   # 确保是Python 3.10.x
   ```

#### 步骤2：安装系统依赖

```bash
sudo apt update
sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip \
    build-essential \
    git \
    curl \
    wget \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    pkg-config
```

详细的系统依赖说明请参考：[SYSTEM_REQUIREMENTS.md](SYSTEM_REQUIREMENTS.md)

#### 步骤3：创建Python虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 步骤4：安装Python依赖

```bash
pip install --upgrade pip
pip install -r requirements_lin.txt
```

#### 步骤5：启动应用

```bash
streamlit run Home.py --server.port=8501 --server.address=0.0.0.0
```

## Docker部署

### 使用Docker Compose（推荐）

1. **构建并启动容器**
   ```bash
   docker-compose -f docker-compose.ubuntu.yml up -d
   ```

2. **查看日志**
   ```bash
   docker-compose -f docker-compose.ubuntu.yml logs -f
   ```

3. **停止服务**
   ```bash
   docker-compose -f docker-compose.ubuntu.yml down
   ```

### 使用Docker

1. **构建镜像**
   ```bash
   docker build -f Dockerfile.ubuntu -t llm-demo:ubuntu .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     --name llm-demo-ubuntu \
     -p 8501:8501 \
     -v ~/.cache/huggingface:/root/.cache/huggingface \
     llm-demo:ubuntu
   ```

## 配置说明

### 环境变量

项目提供了 `.env.ubuntu` 配置文件，包含以下主要配置：

- `STREAMLIT_SERVER_PORT=8501`: Streamlit服务端口
- `HF_HOME=~/.cache/huggingface/`: Hugging Face模型缓存目录
- `TORCH_HOME=~/.cache/torch/`: PyTorch模型缓存目录

### 模型配置

项目使用以下模型：
- **中文模型**: Qwen/Qwen2-1.5B
- **英文模型**: GPT-2

首次运行时，模型会自动从Hugging Face下载到缓存目录。

## 故障排除

### 常见问题

1. **模型下载失败**
   ```bash
   # 设置镜像源
   export HF_ENDPOINT=https://hf-mirror.com
   ```

2. **内存不足**
   ```bash
   # 限制线程数
   export OMP_NUM_THREADS=2
   export MKL_NUM_THREADS=2
   ```

3. **端口被占用**
   ```bash
   # 检查端口占用
   sudo netstat -tlnp | grep 8501
   
   # 使用其他端口
   streamlit run Home.py --server.port=8502
   ```

4. **权限问题**
   ```bash
   # 确保脚本有执行权限
   chmod +x deploy_ubuntu.sh
   chmod +x start_app.sh
   ```

5. **中文字体显示问题**
   ```bash
   # 运行字体修复脚本
   ./fix_fonts.sh

   # 或者手动修复
   sudo apt install -y fonts-noto-cjk fonts-wqy-zenhei
   sudo fc-cache -fv
   ```

6. **Streamlit版本兼容性问题**
   ```bash
   # 如果遇到 use_container_width 错误
   ./fix_streamlit_compatibility.sh

   # 或者手动升级Streamlit
   pip install streamlit==1.39.0
   ```

### 日志查看

- **Streamlit日志**: 直接在终端查看
- **系统日志**: `journalctl -f`
- **Docker日志**: `docker logs llm-demo-ubuntu`

## 性能优化

### 硬件要求

- **最低配置**: 4GB RAM, 2核CPU, 10GB存储
- **推荐配置**: 8GB+ RAM, 4核+ CPU, 20GB+ 存储
- **GPU支持**: 可选，支持NVIDIA GPU加速

### 优化建议

1. **使用SSD存储**提高模型加载速度
2. **增加内存**减少模型加载时间
3. **使用GPU**加速推理（需要CUDA支持）

## 安全注意事项

1. **防火墙配置**
   ```bash
   sudo ufw allow 8501/tcp
   ```

2. **反向代理**（生产环境推荐）
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 更新和维护

### 更新代码

```bash
git pull origin deploy-ubuntu
pip install -r requirements_lin.txt --upgrade
```

### 清理缓存

```bash
# 清理模型缓存
rm -rf ~/.cache/huggingface/
rm -rf ~/.cache/torch/

# 清理Python缓存
find . -type d -name "__pycache__" -exec rm -rf {} +
```

## 支持和反馈

如果在部署过程中遇到问题，请：

1. 检查系统要求是否满足
2. 查看错误日志
3. 参考故障排除部分
4. 提交Issue到项目仓库

---

**注意**: 首次运行时需要下载模型文件（约2-3GB），请确保网络连接稳定。
