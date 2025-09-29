import json
import random

with open('D:\\LLM_project\\LightRAG_learning\\fine-tune_reranker\\generated_data_pairs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

datasets = []

for entry in data:
    query = entry["question"]
    pos = [entry["answerable_string"]]

    all_string = [e["answerable_string"] for e in data if e["answerable_string"]!= entry["answerable_string"] ]

    neg = random.sample(all_string, 10)

    new_entry = {
        "query": query,
        "pos": pos,
        "neg": neg
    }
    datasets.append(new_entry)

#训练：测试 = 9：1
train_size = int( len(datasets)*0.9 )
train_data = datasets[:train_size]
test_data = datasets[train_size:]

#保存测试集
with open('D:\\LLM_project\\LightRAG_learning\\fine-tune_reranker\\test_data.json', 'w', encoding='utf-8') as f:
    json.dump(test_data, f, ensure_ascii=False, indent=4)

#保存测试集
with open('D:\\LLM_project\\LightRAG_learning\\fine-tune_reranker\\train_data.json', 'w', encoding='utf-8') as f:
    for sample in train_data:
        json.dump(sample, f, ensure_ascii=False)
        f.write('\n')

print("Train dataset and Test dataset have been generated")