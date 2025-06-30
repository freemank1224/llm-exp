#!/bin/bash

# Streamlit版本兼容性修复脚本
# 解决旧版本Streamlit不支持use_container_width参数的问题

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

# 检查Streamlit版本
check_streamlit_version() {
    log_info "检查Streamlit版本..."
    
    if [[ -d "venv" ]]; then
        source venv/bin/activate
    fi
    
    # 获取Streamlit版本
    STREAMLIT_VERSION=$(python3 -c "import streamlit; print(streamlit.__version__)" 2>/dev/null || echo "未安装")
    
    if [[ "$STREAMLIT_VERSION" == "未安装" ]]; then
        log_error "Streamlit未安装"
        return 1
    fi
    
    log_info "当前Streamlit版本: $STREAMLIT_VERSION"
    
    # 检查版本是否支持use_container_width
    python3 -c "
import streamlit as st
import sys
from packaging import version

current_version = version.parse('$STREAMLIT_VERSION')
required_version = version.parse('1.2.0')

if current_version < required_version:
    print('需要升级')
    sys.exit(1)
else:
    print('版本兼容')
    sys.exit(0)
" 2>/dev/null
    
    VERSION_CHECK=$?
    if [[ $VERSION_CHECK -eq 1 ]]; then
        log_warning "Streamlit版本过低，不支持use_container_width参数"
        return 1
    else
        log_success "Streamlit版本兼容"
        return 0
    fi
}

# 升级Streamlit
upgrade_streamlit() {
    log_info "升级Streamlit到兼容版本..."
    
    if [[ -d "venv" ]]; then
        source venv/bin/activate
    fi
    
    # 升级到requirements_lin.txt中指定的版本
    pip install streamlit==1.39.0
    
    log_success "Streamlit升级完成"
}

# 创建兼容性检查脚本
create_compatibility_check() {
    log_info "创建兼容性检查脚本..."
    
    cat > check_streamlit_features.py << 'EOF'
"""
Streamlit功能兼容性检查脚本
"""

import streamlit as st
import sys
from packaging import version

def check_streamlit_compatibility():
    """检查Streamlit版本兼容性"""
    
    current_version = version.parse(st.__version__)
    
    print(f"当前Streamlit版本: {st.__version__}")
    
    # 检查各个功能的支持情况
    features = {
        'use_container_width': version.parse('1.2.0'),
        'st.columns': version.parse('0.68.0'),
        'st.tabs': version.parse('1.10.0'),
        'st.toggle': version.parse('1.27.0'),
        'st.divider': version.parse('1.14.0'),
    }
    
    print("\n功能支持情况:")
    all_supported = True
    
    for feature, required_version in features.items():
        if current_version >= required_version:
            print(f"✅ {feature}: 支持")
        else:
            print(f"❌ {feature}: 不支持 (需要 >= {required_version})")
            all_supported = False
    
    if all_supported:
        print("\n✅ 所有功能都支持")
        return True
    else:
        print("\n❌ 部分功能不支持，建议升级Streamlit")
        return False

if __name__ == "__main__":
    supported = check_streamlit_compatibility()
    sys.exit(0 if supported else 1)
EOF

    log_success "兼容性检查脚本创建完成"
}

# 修复label警告
fix_label_warnings() {
    log_info "修复label警告..."
    
    # 创建label修复脚本
    cat > fix_labels.py << 'EOF'
"""
修复Streamlit label警告的脚本
"""

import re
import os

def fix_empty_labels_in_file(filepath):
    """修复文件中的空label问题"""
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复常见的空label问题
    patterns = [
        # st.radio with empty label
        (r'st\.radio\(\s*""\s*,', 'st.radio("选项", '),
        # st.selectbox with empty label  
        (r'st\.selectbox\(\s*""\s*,', 'st.selectbox("请选择", '),
        # st.text_input with empty label
        (r'st\.text_input\(\s*""\s*,', 'st.text_input("输入", '),
        # st.number_input with empty label
        (r'st\.number_input\(\s*""\s*,', 'st.number_input("数值", '),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已修复 {filepath} 中的label问题")
        return True
    
    return False

def main():
    """主函数"""
    
    # 扫描所有Python文件
    python_files = []
    for root, dirs, files in os.walk('.'):
        # 跳过虚拟环境和缓存目录
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git']]
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    fixed_files = []
    for filepath in python_files:
        if fix_empty_labels_in_file(filepath):
            fixed_files.append(filepath)
    
    if fixed_files:
        print(f"\n修复了 {len(fixed_files)} 个文件的label问题:")
        for filepath in fixed_files:
            print(f"  - {filepath}")
    else:
        print("\n未发现需要修复的label问题")

if __name__ == "__main__":
    main()
EOF

    # 运行label修复脚本
    if [[ -d "venv" ]]; then
        source venv/bin/activate
    fi
    
    python3 fix_labels.py
    
    log_success "Label警告修复完成"
}

# 主函数
main() {
    log_info "开始修复Streamlit兼容性问题..."
    
    # 检查版本
    if check_streamlit_version; then
        log_success "Streamlit版本兼容，无需升级"
    else
        log_warning "检测到版本兼容性问题"
        read -p "是否要升级Streamlit? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            upgrade_streamlit
        else
            log_info "跳过Streamlit升级"
        fi
    fi
    
    # 创建兼容性检查工具
    create_compatibility_check
    
    # 修复label警告
    fix_label_warnings
    
    log_success "Streamlit兼容性修复完成！"
    echo ""
    log_info "修复内容："
    log_info "1. 移除了所有use_container_width参数（已在代码中完成）"
    log_info "2. 创建了兼容性检查脚本 check_streamlit_features.py"
    log_info "3. 修复了可能的label警告问题"
    echo ""
    log_info "使用方法："
    log_info "  python3 check_streamlit_features.py  # 检查功能支持"
}

# 执行主函数
main "$@"
