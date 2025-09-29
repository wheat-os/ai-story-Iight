import json
from zhipuai import ZhipuAI
from tqdm import tqdm

#给出智谱api key以调用接口
client = ZhipuAI(api_key="c38e4f744d60488d9aeeaacd92658ba2.1HtkH0CTPssEX4BM")

def generate_questions(text):
    response = client.chat.completions.create(
        model = "glm-4-flashx",
        messages=[
            {"role":"system", "content":"You are a helpful assitant."},
            {"role":"user", "content": f"生成一个和给定文本相关的问题，用于检索数据集的构建。请只给出对应文本的问题，但不要有其他多余语言\n 文本:{text}"}
        ],
        stream = False
    )

    res = response.choices[0].message.content
    print('res', res)
    return res

with open('D:\\LLM_project\\LightRAG_learning\\fine-tune_reranker\\all_samples_string.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

#构造数据对
dataset = []

for sample in tqdm(data['sample']):
    question = generate_questions(sample)

    dataset_entry = {
        "question":question,
        "answerable_string":sample
    }

    dataset.append(dataset_entry)

with open('D:\\LLM_project\\LightRAG_learning\\fine-tune_reranker\\generated_data_pairs.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)

print("Questions have been generated")