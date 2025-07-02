from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import torch.nn.functional as F
import os
import warnings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 添加更多具体的警告过滤
warnings.filterwarnings('ignore', category=UserWarning, message='.*torch.classes.*')
warnings.filterwarnings('ignore', category=UserWarning, message='.*Trying to initialize.*')

# 禁用 SSL 警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

os.environ['CURL_CA_BUNDLE'] = ''

class LLMPredictor:
    def __init__(self):
        # 在Docker环境中使用镜像内的缓存目录，否则使用用户主目录
        if os.path.exists("/app/models"):
            self.cache_dir = "/app/models"
        else:
            self.cache_dir = os.path.expanduser("~/.cache/huggingface/")
        
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 预初始化设备
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")
            
        print(f"Using device: {self.device}")
        print(f"Using cache directory: {self.cache_dir}")
        
        # 统一使用 Qwen2-1.5B 模型处理中英文
        self.model_name = "Qwen/Qwen2-1.5B"
        self.model = None
        self.tokenizer = None
        self.current_lang = None

    def _load_unified_model(self):
        """加载统一的 Qwen2-1.5B 模型，用于处理中英文"""
        if self.model is None:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name,
                    trust_remote_code=True,
                    cache_dir=self.cache_dir
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    trust_remote_code=True,
                    cache_dir=self.cache_dir
                )
                self.model.to(self.device)
                print(f"Unified model {self.model_name} is loaded on {self.device}")
                return True
            except Exception as e:
                print(f"加载统一模型失败: {str(e)}")
                return False
        return True

    def _get_model_and_tokenizer(self, model_lang):
        """获取统一的模型和分词器（不再区分语言）"""
        if not self._load_unified_model():
            raise ValueError("无法加载统一模型")
        # 为了兼容性，添加语言相关的属性访问
        if model_lang == "中文":
            self.zh_model = self.model
            self.zh_tokenizer = self.tokenizer
        else:
            self.en_model = self.model  
            self.en_tokenizer = self.tokenizer
        return self.model, self.tokenizer

    def generate_next_token(self, input_text, model_lang = "中文", temperature = 1.0, top_k = 8):
        # 1. Encode the input text
        try:
            active_model, active_tokenizer = self._get_model_and_tokenizer(model_lang)
            input_ids = active_tokenizer.encode(input_text, return_tensors='pt').to(self.device)

            with torch.no_grad():
                outputs = active_model(input_ids)
                logits = outputs.logits

            # Get the output logits and transformed to probabilities
            next_token_logits = logits[0, -1, :]
            next_token_probs = F.softmax(next_token_logits, dim=-1)

            # Apply temperature to alter relative weights
            if temperature != 0:
                next_token_probs = next_token_probs / temperature

            topk_probs, topk_indices = torch.topk(next_token_probs, top_k)

            topk_probs = F.softmax(topk_probs, dim=-1)

            chosen_idx = torch.multinomial(topk_probs, 1)

            print(f"Top {top_k} next token predictions were generated!")
            print(f"Top K index is: {topk_indices}")
            print(f"The Chosen token is: {chosen_idx.item()}")

            # Establish return results
            results = []

            for tid, prob in zip(topk_indices, topk_probs):
                token = active_tokenizer.decode(tid.item())
                results.append({
                    'token': token,
                    'probability': float(prob),
                    'is_sampled': True if tid==topk_indices[chosen_idx.item()] else False
                })


            return {
                'language': model_lang,
                'input_text': input_text,
                'predictions': results
            }
        
        except Exception as e:
            raise Exception(f"处理过程出现错误: {str(e)}.")

    
    def predict_next_token(self, input_text, *, temperature=1.0, model_lang="中文", top_k=10):
        """
        预测下一个token并使用Top-K随机采样
        
        参数:
            input_text (str): 输入文本
            temperature (float): 温度参数，默认为1.0
            model_lang (str): 模型语言，默认为"中文"
            top_k (int): 返回的top k个结果，默认为10
        """
        try:
            model, tokenizer = self._get_model_and_tokenizer(model_lang)
            input_ids = tokenizer.encode(input_text, return_tensors='pt', add_special_tokens=True)

            with torch.no_grad():
                outputs = model(input_ids)
                logits = outputs.logits

            # 获取最后一个位置的 logits
            last_token_logits = logits[:, -1, :]
            
            # 应用温度
            if temperature != 1.0:
                last_token_logits = last_token_logits / temperature

            # 计算概率分布
            probabilities = torch.softmax(last_token_logits, dim=-1)

            # 获取概率最高的 K 个 tokens
            topk_probs, topk_indices = torch.topk(probabilities, top_k)
            
            # 对top-k的概率进行归一化
            topk_probs = torch.softmax(topk_probs, dim=-1)
            
            # 使用归一化后的概率进行随机采样
            chosen_idx = torch.multinomial(topk_probs[0], 1)
            
            # 重新排序tokens，将采样到的token放在第一位
            selected_token = topk_indices[0][chosen_idx]
            selected_prob = topk_probs[0][chosen_idx]
            
            # 获取所有候选tokens
            topk_tokens = tokenizer.convert_ids_to_tokens(topk_indices[0])
            
            # 构建返回结果，确保采样的token在第一位
            results = []
            selected_token_str = tokenizer.convert_ids_to_tokens(selected_token)[0]
            results.append({
                'token': selected_token_str,
                'probability': float(selected_prob),
                'is_sampled': True
            })
            
            # 添加其他候选tokens
            for token, prob in zip(topk_tokens, topk_probs[0].tolist()):
                if token != selected_token_str:
                    results.append({
                        'token': token,
                        'probability': round(prob, 4),
                        'is_sampled': False
                    })

            return {
                'language': model_lang,
                'input_text': input_text,
                'predictions': results
            }

        except Exception as e:
            raise Exception(f"预测过程中出现错误: {str(e)}")

