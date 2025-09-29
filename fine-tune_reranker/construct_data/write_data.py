import json
import random

with open('D:\\LLM_project\\LightRAG_learning\\fine-tune_reranker\\vdb_entities.json', 'r', encoding= 'utf-8') as f:
    edata = json.load(f)
print( len(edata['data']))

with open('D:\\LLM_project\\LightRAG_learning\\fine-tune_reranker\\vdb_relationships.json', 'r', encoding= 'utf-8') as f:
    rdata = json.load(f)
print( len(rdata['data']))


nodes_samples = random.sample(edata['data'], 500)
edges_samples = random.sample(rdata['data'], 500)

new_data = {
    'nodes': nodes_samples,
    'edges': edges_samples
}

with open('D:\\LLM_project\\LightRAG_learning\\fine-tune_reranker\\sampled_data.json', 'w', encoding= 'utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)

print("500 data of edge and entity have been generated")