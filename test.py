from transformers import GPT2Tokenizer, GPT2LMHeadModel, BertTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import torch.nn.functional as F
import os
import numpy as np

cache_dir = os.path.expanduser("~/.cache/huggingface/")
os.makedirs(cache_dir, exist_ok=True)

try:
    tokenizer = AutoTokenizer.from_pretrained('gpt2', cache_dir=cache_dir)
    # print(f"Tokenizer loaded as: {tokenizer}")
    llm = AutoModelForCausalLM.from_pretrained('gpt2', cache_dir=cache_dir)
    # print(f"LLM loaded as: {llm}")

except Exception as e:
    print(f"Model loaded failed: {str(e)}")

input_text = "This is one small step for man "
input_ids = tokenizer.encode(input_text, return_tensors='pt')
print(input_ids)
print("-------- OUTPUT ---------")

with torch.no_grad():
    outputs = llm(input_ids)
    # Shape: [batch_size, sequence_size, vocab_size]
    logits = outputs.logits[0, -1, :]
    print(f"Logits Shape: {logits.shape}")
    
    k = 5
    top_k_scores, top_k_idx = torch.topk(logits, k)
    # Transform to probabilities
    top_k_probs = F.softmax(top_k_scores, dim=-1)

    print(f"\nTop K Sampling(k={k}):")
    for i, (idx, prob) in enumerate(zip(top_k_idx, top_k_probs)):
        token = tokenizer.decode([idx.item()])
        print(f"Candidate{i+1}: '{token}' (Probability: {prob:4f})")

    next_token_idx = top_k_idx[torch.multinomial(top_k_probs, num_samples=1)]
    print(f"\nSampled Token: '{tokenizer.decode([next_token_idx.item()])}'")
