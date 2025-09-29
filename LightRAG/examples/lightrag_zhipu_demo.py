import os
import logging

from lightrag import LightRAG, QueryParam
from lightrag.llm.zhipu import zhipu_complete, zhipu_embedding
from lightrag.utils import EmbeddingFunc

WORKING_DIR = "./dickens"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

api_key = os.environ.get("ZHIPUAI_API_KEY")
if api_key is None:
    raise Exception("Please set ZHIPU_API_KEY in your environment")


rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=zhipu_complete,
    llm_model_name="glm-4-flashx",  # Using the most cost/performance balance model, but you can change it here.
    llm_model_max_async=4,
    llm_model_max_token_size=32768,
    embedding_func=EmbeddingFunc(
        embedding_dim=2048,  # Zhipu embedding-3 dimension
        max_token_size=8192,
        func=lambda texts: zhipu_embedding(texts),
    ),
)







fd_path = "D:\\LLM_project\\LightRAG_learning\\doc"

# for filename in os.listdir(fd_path):
#     # 检查是否为txt文件
#     if filename.endswith(".txt"): 
#         # 构造完整的文件路径
#         file_path = os.path.join(fd_path, filename)
#         with open(file_path, "r", encoding="utf-8") as f:
#             # 读取文件内容并插入到 rag 中
#             rag.insert(f.read())

# # Perform naive search
# print(
#     rag.query("What are the top themes in this story?", param=QueryParam(mode="naive"))
# )

# # Perform local search
# print(
#     rag.query("What are the top themes in this story?", param=QueryParam(mode="local"))
# )

# # Perform global search
# print(
#     rag.query("What are the top themes in this story?", param=QueryParam(mode="global"))
# )

# Perform hybrid search
print(
    rag.query("韩立都有哪些朋友", param=QueryParam(mode="hybrid"))
)
