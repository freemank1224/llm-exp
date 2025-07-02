#!/usr/bin/env python3
# 简单测试脚本，验证统一模型是否工作

from model import LLMPredictor
import sys

def test_unified_model():
    print("=== 测试统一模型 (Qwen2-1.5B) ===")
    
    try:
        # 创建预测器
        predictor = LLMPredictor()
        print("✓ LLMPredictor 创建成功")
        
        # 测试中文
        print("\n--- 测试中文文本 ---")
        chinese_text = "大家好，我是"
        result_zh = predictor.generate_next_token(chinese_text, model_lang="中文", top_k=3)
        print(f"输入: {chinese_text}")
        print("预测结果:")
        for pred in result_zh['predictions']:
            print(f"  {pred['token']} - 概率: {pred['probability']:.4f}")
        
        # 测试英文
        print("\n--- 测试英文文本 ---")
        english_text = "Hello, I am"
        result_en = predictor.generate_next_token(english_text, model_lang="英文", top_k=3)
        print(f"输入: {english_text}")
        print("预测结果:")
        for pred in result_en['predictions']:
            print(f"  {pred['token']} - 概率: {pred['probability']:.4f}")
            
        print("\n✓ 统一模型测试完成！")
        print(f"✓ 中英文都使用同一个模型: {predictor.model_name}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_unified_model()
