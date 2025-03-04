# 假设你的列表变量名为 tokens_list
tokens_list = [
    {'token': 'token1', 'prob': 0.1, 'flag': True},
    {'token': 'token2', 'prob': 0.2, 'flag': False},
    {'token': 'token3', 'prob': 0.3, 'flag': False}
]

# 过滤出 flag 为 True 的项，并提取 token 值
selected_tokens = [item['token'] for item in tokens_list if item['flag']]
# selected_tokens = item['token'] for item in tokens_list if item['flag']

print(selected_tokens[0])