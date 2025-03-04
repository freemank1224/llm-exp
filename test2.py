test_list = [
    {'token': 'token1', 'prob': 0.1, 'is_sampled': False},
    {'token': 'token2', 'prob': 0.2, 'is_sampled': True},
    {'token': 'token3', 'prob': 0.3, 'is_sampled': False}
]

# print(test_list)

for element in test_list:
    print(element)
    print(f"The is_sampled flag is: {element['is_sampled']}")
    flag = element.get('is_sampled', True)
    print(flag)