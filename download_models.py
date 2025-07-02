#!/usr/bin/env python3
"""
模型预下载脚本
在Docker构建时下载模型到镜像缓存中
"""

import os
import warnings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from transformers import AutoTokenizer, AutoModelForCausalLM

# 添加更多具体的警告过滤
warnings.filterwarnings('ignore', category=UserWarning, message='.*torch.classes.*')
warnings.filterwarnings('ignore', category=UserWarning, message='.*Trying to initialize.*')

# 禁用 SSL 警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 设置环境变量
os.environ['CURL_CA_BUNDLE'] = ''

def download_models():
    """下载所需的模型到指定缓存目录"""
    
    # 设置缓存目录
    cache_dir = "/app/models"
    os.makedirs(cache_dir, exist_ok=True)
    
    # 要下载的模型列表
    models_to_download = [
        "Qwen/Qwen2-1.5B"
    ]
    
    print("开始下载模型到Docker镜像缓存...")
    
    for model_name in models_to_download:
        try:
            print(f"正在下载模型: {model_name}")
            
            # 下载tokenizer
            print(f"  - 下载tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True,
                cache_dir=cache_dir
            )
            
            # 下载模型
            print(f"  - 下载模型权重...")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                cache_dir=cache_dir
            )
            
            print(f"✅ 模型 {model_name} 下载完成")
            
            # 清理内存
            del model
            del tokenizer
            
        except Exception as e:
            print(f"❌ 下载模型 {model_name} 失败: {str(e)}")
            raise e
    
    print("🎉 所有模型下载完成！")
    
    # 打印缓存目录大小信息
    try:
        import subprocess
        result = subprocess.run(['du', '-sh', cache_dir], capture_output=True, text=True)
        print(f"模型缓存目录大小: {result.stdout.strip()}")
    except:
        pass

if __name__ == "__main__":
    download_models()
