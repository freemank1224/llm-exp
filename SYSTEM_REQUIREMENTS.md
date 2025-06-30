# Ubuntu 22.04 系统依赖安装指南

## 系统要求

- **操作系统**: Ubuntu 22.04 LTS
- **Python版本**: Python 3.10
- **内存**: 至少 4GB RAM（推荐 8GB+）
- **存储**: 至少 10GB 可用空间（用于模型缓存）
- **网络**: 稳定的互联网连接（用于下载模型）

## 系统包依赖

### 基础开发工具

```bash
sudo apt update
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    pkg-config
```

### Python相关

```bash
sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip
```

### 图像处理库

```bash
sudo apt install -y \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libtiff5-dev \
    libwebp-dev \
    libopenjp2-7-dev
```

### SSL和加密库

```bash
sudo apt install -y \
    libssl-dev \
    libffi-dev \
    libcrypt-dev
```

### 数学和科学计算库

```bash
sudo apt install -y \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran
```

### 中文字体支持（重要！）

```bash
sudo apt install -y \
    fonts-noto-cjk \
    fonts-noto-cjk-extra \
    fonts-wqy-zenhei \
    fonts-wqy-microhei \
    fonts-arphic-ukai \
    fonts-arphic-uming \
    fonts-liberation \
    fontconfig

# 更新字体缓存
sudo fc-cache -fv
```

### 可选：GPU支持（如果有NVIDIA GPU）

```bash
# NVIDIA驱动（根据你的GPU型号选择合适版本）
sudo apt install -y nvidia-driver-525

# CUDA工具包（可选，PyTorch会自带CUDA运行时）
# wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
# sudo dpkg -i cuda-keyring_1.0-1_all.deb
# sudo apt update
# sudo apt install -y cuda-toolkit-12-0
```

## 一键安装脚本

所有系统依赖可以通过以下命令一次性安装：

```bash
sudo apt update && sudo apt install -y \
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
    libtiff5-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    pkg-config \
    fonts-noto-cjk \
    fonts-noto-cjk-extra \
    fonts-wqy-zenhei \
    fonts-wqy-microhei \
    fonts-arphic-ukai \
    fonts-arphic-uming \
    fonts-liberation \
    fontconfig

# 更新字体缓存
sudo fc-cache -fv
```

## 验证安装

### 检查Python版本

```bash
python3 --version
# 应该显示: Python 3.10.x
```

### 检查pip

```bash
python3 -m pip --version
# 应该显示pip版本信息
```

### 检查开发工具

```bash
gcc --version
make --version
git --version
```

## 常见问题解决

### 1. Python版本不是3.10

如果系统默认Python不是3.10，可以使用以下方法：

```bash
# 安装python3.10
sudo apt install python3.10 python3.10-venv python3.10-dev

# 创建符号链接（可选）
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
```

### 2. pip安装失败

```bash
# 重新安装pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.10 get-pip.py --user
```

### 3. 编译错误

如果在安装Python包时遇到编译错误，确保安装了所有开发工具：

```bash
sudo apt install -y build-essential python3.10-dev
```

### 4. 图像处理库错误

如果Pillow安装失败：

```bash
sudo apt install -y libjpeg-dev libpng-dev libfreetype6-dev
pip install --upgrade pip
pip install Pillow --force-reinstall
```

### 5. 中文字体显示问题

如果遇到中文字体显示问题或字体警告：

```bash
# 运行字体修复脚本
./fix_fonts.sh

# 或者手动安装字体
sudo apt install -y fonts-noto-cjk fonts-wqy-zenhei
sudo fc-cache -fv

# 清除matplotlib字体缓存
python3 -c "import matplotlib.font_manager as fm; fm._rebuild()"
```

## 性能优化建议

### 1. 内存优化

对于内存较小的系统，可以设置环境变量：

```bash
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
```

### 2. 存储优化

模型文件会缓存在 `~/.cache/huggingface/`，确保有足够空间：

```bash
# 检查可用空间
df -h ~/.cache/

# 如果空间不足，可以设置自定义缓存目录
export HF_HOME=/path/to/large/storage/.cache/huggingface/
```

### 3. 网络优化

如果下载模型较慢，可以设置镜像源：

```bash
# 使用清华大学镜像
export HF_ENDPOINT=https://hf-mirror.com
```
