#!/bin/bash

# Ubuntu 22.04 + Python 3.10 部署脚本
# 大语言模型演示项目部署脚本

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查系统版本
check_system() {
    log_info "检查系统版本..."
    
    if [[ ! -f /etc/os-release ]]; then
        log_error "无法检测系统版本"
        exit 1
    fi
    
    source /etc/os-release
    
    if [[ "$ID" != "ubuntu" ]]; then
        log_error "此脚本仅支持Ubuntu系统，当前系统: $ID"
        exit 1
    fi
    
    if [[ "$VERSION_ID" != "22.04" ]]; then
        log_warning "推荐使用Ubuntu 22.04，当前版本: $VERSION_ID"
    fi
    
    log_success "系统检查通过: $PRETTY_NAME"
}

# 检查Python版本
check_python() {
    log_info "检查Python版本..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python3未安装"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    
    if [[ "$PYTHON_VERSION" != "3.10" ]]; then
        log_warning "推荐使用Python 3.10，当前版本: $PYTHON_VERSION"
    fi
    
    log_success "Python版本检查通过: $PYTHON_VERSION"
}

# 安装系统依赖
install_system_deps() {
    log_info "安装系统依赖..."

    sudo apt update

    # 安装必要的系统包
    sudo apt install -y \
        python3-pip \
        python3-venv \
        python3-dev \
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

    # 安装中文字体支持
    log_info "安装中文字体支持..."
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

    log_success "系统依赖和字体安装完成"
}

# 创建虚拟环境
create_venv() {
    log_info "创建Python虚拟环境..."
    
    if [[ -d "venv" ]]; then
        log_warning "虚拟环境已存在，跳过创建"
        return
    fi
    
    python3 -m venv venv
    log_success "虚拟环境创建完成"
}

# 激活虚拟环境并安装依赖
install_deps() {
    log_info "激活虚拟环境并安装Python依赖..."
    
    source venv/bin/activate
    
    # 升级pip
    pip install --upgrade pip
    
    # 安装依赖
    if [[ -f "requirements_lin.txt" ]]; then
        pip install -r requirements_lin.txt
        log_success "Python依赖安装完成"
    else
        log_error "requirements_lin.txt文件不存在"
        exit 1
    fi
}

# 检查模型下载
check_models() {
    log_info "检查模型文件..."
    
    # 创建缓存目录
    mkdir -p ~/.cache/huggingface/
    
    log_warning "首次运行时，模型将自动从Hugging Face下载"
    log_warning "请确保网络连接正常，下载可能需要较长时间"
    
    log_success "模型检查完成"
}

# 创建启动脚本
create_start_script() {
    log_info "创建启动脚本..."

    cat > start_app.sh << 'EOF'
#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 设置环境变量
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export MPLBACKEND=Agg
export PYTHONWARNINGS=ignore::UserWarning

# 加载Ubuntu环境配置
if [[ -f ".env.ubuntu" ]]; then
    source .env.ubuntu
fi

# 启动Streamlit应用
echo "启动大语言模型演示应用..."
echo "应用将在 http://localhost:8501 启动"
echo "按 Ctrl+C 停止应用"

# 使用带字体修复的启动方式
streamlit run app_with_font_fix.py --server.port=8501 --server.address=0.0.0.0
EOF

    chmod +x start_app.sh
    log_success "启动脚本创建完成"
}

# 主函数
main() {
    log_info "开始Ubuntu 22.04部署流程..."
    
    check_system
    check_python
    install_system_deps
    create_venv
    install_deps
    check_models
    create_start_script
    
    log_success "部署完成！"
    echo ""
    log_info "使用方法："
    log_info "1. 运行 ./start_app.sh 启动应用"
    log_info "2. 在浏览器中访问 http://localhost:8501"
    log_info "3. 按 Ctrl+C 停止应用"
    echo ""
    log_warning "注意：首次运行时需要下载模型文件，请保持网络连接"
}

# 执行主函数
main "$@"
