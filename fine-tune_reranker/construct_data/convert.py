import json

#读取知识图谱数据（包括边和节点）
with open('D:\\LLM_project\\LightRAG_learning\\fine-tune_reranker\\sampled_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

#创建个列表存储所有边和节点拼接得到的字符串 作为正例
all_strings = []

#拼接所有节点数据
for node in data['nodes']:
    node_str = f"{node['content']}"
    all_strings.append(node_str)

for edge in data['edges']:
    edge_str = f"{edge['src_id']} {edge['tgt_id']} {edge['content']}"
    all_strings.append(edge_str)

new_data = {
    'sample': all_strings
}

with open('D:\\LLM_project\\LightRAG_learning\\fine-tune_reranker\\all_samples_string.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)

print("sample data have been concated")