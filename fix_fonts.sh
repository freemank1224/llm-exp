#!/bin/bash

# Ubuntu 中文字体修复脚本
# 解决Streamlit中文显示和matplotlib字体问题

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# 安装中文字体
install_chinese_fonts() {
    log_info "安装中文字体..."
    
    # 更新包列表
    sudo apt update
    
    # 安装中文字体包
    sudo apt install -y \
        fonts-noto-cjk \
        fonts-noto-cjk-extra \
        fonts-wqy-zenhei \
        fonts-wqy-microhei \
        fonts-arphic-ukai \
        fonts-arphic-uming \
        fonts-liberation \
        fontconfig
    
    log_success "中文字体安装完成"
}

# 配置matplotlib字体
configure_matplotlib() {
    log_info "配置matplotlib字体..."
    
    # 激活虚拟环境（如果存在）
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
        log_info "已激活虚拟环境"
    fi
    
    # 创建matplotlib配置脚本
    cat > configure_matplotlib_fonts.py << 'EOF'
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 设置matplotlib后端
matplotlib.use('Agg')

# 查找可用的中文字体
def find_chinese_fonts():
    """查找系统中可用的中文字体"""
    chinese_fonts = []
    
    # 常见的中文字体名称
    font_names = [
        'Noto Sans CJK SC',
        'Noto Sans CJK TC', 
        'WenQuanYi Zen Hei',
        'WenQuanYi Micro Hei',
        'AR PL UKai CN',
        'AR PL UMing CN',
        'DejaVu Sans',
        'Liberation Sans'
    ]
    
    for font_name in font_names:
        try:
            font_path = fm.findfont(fm.FontProperties(family=font_name))
            if font_path and os.path.exists(font_path):
                chinese_fonts.append(font_name)
                print(f"找到字体: {font_name} -> {font_path}")
        except:
            continue
    
    return chinese_fonts

# 配置matplotlib字体
def configure_fonts():
    """配置matplotlib使用中文字体"""
    
    # 清除字体缓存
    try:
        fm._rebuild()
        print("字体缓存已清除")
    except:
        pass
    
    # 查找中文字体
    chinese_fonts = find_chinese_fonts()
    
    if chinese_fonts:
        # 使用第一个找到的中文字体
        font_name = chinese_fonts[0]
        plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        print(f"已配置matplotlib使用字体: {font_name}")
        
        # 测试中文显示
        try:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.text(0.5, 0.5, '测试中文显示', fontsize=16, ha='center', va='center')
            ax.set_title('中文字体测试')
            plt.savefig('font_test.png', dpi=100, bbox_inches='tight')
            plt.close()
            print("中文字体测试成功，已生成 font_test.png")
        except Exception as e:
            print(f"字体测试失败: {e}")
    else:
        print("警告: 未找到合适的中文字体")
    
    return chinese_fonts

if __name__ == "__main__":
    print("=== matplotlib 字体配置 ===")
    fonts = configure_fonts()
    print(f"可用中文字体: {fonts}")
EOF

    # 运行字体配置脚本
    python3 configure_matplotlib_fonts.py
    
    log_success "matplotlib字体配置完成"
}

# 创建字体配置文件
create_font_config() {
    log_info "创建应用字体配置..."
    
    # 创建字体配置Python模块
    cat > font_config.py << 'EOF'
"""
字体配置模块
解决中文显示问题
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings
import os

# 设置matplotlib后端
matplotlib.use('Agg')

def setup_chinese_fonts():
    """设置中文字体支持"""
    
    # 禁用字体相关警告
    warnings.filterwarnings('ignore', category=UserWarning, message='.*font.*')
    warnings.filterwarnings('ignore', category=UserWarning, message='.*Glyph.*')
    
    # 中文字体优先级列表
    chinese_fonts = [
        'Noto Sans CJK SC',
        'Noto Sans CJK TC',
        'WenQuanYi Zen Hei', 
        'WenQuanYi Micro Hei',
        'AR PL UKai CN',
        'AR PL UMing CN',
        'SimHei',
        'Microsoft YaHei',
        'DejaVu Sans'
    ]
    
    # 尝试设置字体
    for font_name in chinese_fonts:
        try:
            font_path = fm.findfont(fm.FontProperties(family=font_name))
            if font_path and os.path.exists(font_path):
                plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
                plt.rcParams['axes.unicode_minus'] = False
                print(f"已设置字体: {font_name}")
                return font_name
        except:
            continue
    
    # 如果没有找到中文字体，使用默认设置
    plt.rcParams['axes.unicode_minus'] = False
    print("警告: 未找到中文字体，使用默认字体")
    return None

# 自动执行字体设置
setup_chinese_fonts()
EOF

    log_success "字体配置文件创建完成"
}

# 更新字体缓存
update_font_cache() {
    log_info "更新系统字体缓存..."
    
    # 更新fontconfig缓存
    sudo fc-cache -fv
    
    # 清除matplotlib字体缓存
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
        python3 -c "import matplotlib.font_manager as fm; fm._rebuild()" 2>/dev/null || true
    fi
    
    log_success "字体缓存更新完成"
}

# 修复代码中的label警告
fix_label_warnings() {
    log_info "修复代码中的label警告..."
    
    # 这个警告来自于main.py中的text_area没有proper label
    # 我们需要修复这个问题
    if [[ -f "main.py" ]]; then
        # 备份原文件
        cp main.py main.py.backup
        
        # 修复label问题（这个需要在代码中处理）
        log_warning "请检查main.py中的st.text_area调用，确保都有proper label"
    fi
    
    log_success "Label警告修复提示完成"
}

# 主函数
main() {
    log_info "开始修复Ubuntu中文字体问题..."
    
    install_chinese_fonts
    configure_matplotlib
    create_font_config
    update_font_cache
    fix_label_warnings
    
    log_success "字体修复完成！"
    echo ""
    log_info "修复内容："
    log_info "1. 安装了中文字体包"
    log_info "2. 配置了matplotlib中文字体支持"
    log_info "3. 创建了字体配置模块 font_config.py"
    log_info "4. 更新了系统字体缓存"
    echo ""
    log_warning "请重启Streamlit应用以使字体配置生效"
    log_info "在Python代码中导入: import font_config"
}

# 执行主函数
main "$@"
