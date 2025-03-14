from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.nn.functional import softmax
import torch, os

model_name = "Qwen/Qwen2-1.5B"
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=os.path.expanduser("~/.cache/huggingface/"))
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir = os.path.expanduser("~/.cache/huggingface/"))

print("*"*50)
print(f"词表大小：{len(tokenizer)}")
print("*"*50)

device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def get_next_token_probabilities(input_text, top_n=10):
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits
    last_logits = outputs.logits[:, -1, :]
    probabilities = softmax(last_logits, dim=-1)  # 添加 dim 参数

    top_probs, top_indices = torch.topk(probabilities[0], top_n)
    top_logits = last_logits[0][top_indices]
    # 使用decode而不是convert_ids_to_tokens来更好地处理中文
    top_tokens = [tokenizer.decode([int(idx)]) for idx in top_indices]

    return list(zip(top_tokens, top_probs.cpu(), top_logits.cpu()))

def get_probability_and_logit(input_text, next_token):  
    inputs = tokenizer(input_text, return_tensors="pt").to(device)  
    with torch.no_grad():
        outputs = model(**inputs)  
    last_logits = outputs.logits[:, -1, :]  
    token_id = tokenizer.convert_tokens_to_ids(next_token)  
    if token_id is None:  
        return 0.0, float('-inf') 
    probability = softmax(last_logits, dim=-1)[0][token_id].item()  # 添加 dim 参数
    logit = last_logits[0][token_id].item()  
    return probability, logit

def analyze_next_tokens(input_text, specific_tokens=None, top_n=10):  
    print("\n最可能的", top_n, "个下一个词元：")  
    top_tokens_probs_logits = get_next_token_probabilities(input_text, top_n)  
    for token, prob, logit in top_tokens_probs_logits:  
        # 改进输出格式
        print(f"{token:<10} | 概率: {prob:>7.4f} | Logit: {logit:>8.4f}")  
    
    if specific_tokens:  
        print("\n特定词元的概率和Logit值：")  
        for token in specific_tokens:  
            prob, logit = get_probability_and_logit(input_text, token)  
            print(f"{token:<10} | 概率: {prob:>7.4f} | Logit: {logit:>8.4f}")

input_text = "大家好，我是"
specific_tokens = ["?", "!"]
analyze_next_tokens(input_text, specific_tokens)