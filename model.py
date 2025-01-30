from transformers import GPT2Tokenizer, GPT2LMHeadModel, AutoTokenizer, AutoModelForCausalLM
import torch
import os

class LLMPredictor:
    def __init__(self):
        self.cache_dir = os.path.expanduser("~/.cache/huggingface/")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.zh_model = None
        self.zh_tokenizer = None
        self.en_model = None
        self.en_tokenizer = None
        self.current_lang = None

    def _load_chinese_model(self):
        if self.zh_model is None:
            try:
                self.zh_tokenizer = AutoTokenizer.from_pretrained(
                    "uer/gpt2-chinese-cluecorpussmall",
                    trust_remote_code=True,
                    cache_dir=self.cache_dir
                )
                self.zh_model = AutoModelForCausalLM.from_pretrained(
                    "uer/gpt2-chinese-cluecorpussmall",
                    trust_remote_code=True,
                    cache_dir=self.cache_dir
                )
                self.current_lang = "中文"
            except Exception as e:
                print(f"加载中文模型失败: {str(e)}")
                return False
        return True

    def _load_english_model(self):
        if self.en_model is None:
            try:
                self.en_tokenizer = GPT2Tokenizer.from_pretrained('gpt2', cache_dir=self.cache_dir)
                self.en_model = GPT2LMHeadModel.from_pretrained('gpt2', cache_dir=self.cache_dir)
                # 设置特殊token
                if self.en_tokenizer.pad_token is None:
                    self.en_tokenizer.pad_token = self.en_tokenizer.eos_token
                self.current_lang = "英文"
            except Exception as e:
                print(f"加载英文模型失败: {str(e)}")
                return False
        return True

    def _get_model_and_tokenizer(self, model_lang):
        """获取对应语言的模型和分词器"""
        if model_lang == "中文":
            if not self._load_chinese_model():
                raise ValueError("无法加载中文模型")
            return self.zh_model, self.zh_tokenizer
        else:
            if not self._load_english_model():
                raise ValueError("无法加载英文模型")
            return self.en_model, self.en_tokenizer

    def predict_next_tokens(self, input_text, *, temperature=1.0, model_lang="中文", top_k=10):
        """
        预测下一个token
        
        参数:
            input_text (str): 输入文本
            temperature (float): 温度参数，默认为1.0
            model_lang (str): 模型语言，默认为"中文"
            top_k (int): 返回的top k个结果，默认为10
        """
        try:
            # 获取对应语言的模型和分词器
            model, tokenizer = self._get_model_and_tokenizer(model_lang)

            # 编码输入文本
            input_ids = tokenizer.encode(input_text, return_tensors='pt', add_special_tokens=True)

            # 使用模型生成文本
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

            # 将 token IDs 转换为可读的 tokens
            topk_tokens = tokenizer.convert_ids_to_tokens(topk_indices[0])

            # 构建返回结果
            results = []
            for token, prob in zip(topk_tokens, topk_probs[0].tolist()):
                results.append({
                    'token': token,
                    'probability': round(prob, 4)
                })

            return {
                'language': model_lang,
                'input_text': input_text,
                'predictions': results
            }

        except Exception as e:
            raise Exception(f"预测过程中出现错误: {str(e)}")

