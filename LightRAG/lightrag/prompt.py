from __future__ import annotations
from typing import Any

GRAPH_FIELD_SEP = "<SEP>"

PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "中文"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["矿物种类", "矿物特性", "地质作用", "化学成分", "矿物变化作用","物理化学条件"]

PROMPTS["entity_extraction"] = """---Goal---
给定一份可能与这项活动相关的文本文档以及一份实体类型列表，从文本中识别出属于这些类型的所有实体，并找出已识别实体之间的所有关系。
使用 {language} 作为输出语言。
---Steps---
1.识别所有实体。对于每一个已识别的实体，提取以下信息：
- entity_name: 实体的名称，使用与输入文本相同的语言。如果是英文，将名称首字母大写。
- entity_type: 是接下来类别的其中一种: [{entity_types}]
- entity_description: 对该实体的属性和活动的全面描述
将每个实体格式化为 ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. 从第1步中识别的实体中,确定所有明确相关的 (source_entity, target_entity) 对
对于每一对相关的实体，提取以下信息:
- source_entity: 源实体的名称，即如在步骤 1 中所识别出的名称
- target_entity: 目标实体的名称，即如在步骤 1 中所识别出的名称
- relationship_description: 关于你认为源实体和目标实体彼此相关的原因的解释
- relationship_strength: 一个表示源实体和目标实体之间关系强度的数值分数
- relationship_keywords: 一个或多个概括这种关系总体性质的高级关键词，重点关注概念或主题，而非具体细节
将每个关系格式化为 ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. 识别能够总结整个文本的主要概念、主题或话题的高级关键词。这些关键词应该能够抓住文档中呈现的总体思想。
将内容层面的关键词格式设置为 ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. 按照步骤1和步骤2识别的所有实体和关系, 使用 **{record_delimiter}** 作为列表分隔符,在{language}中返回输出

5. 完成时, 输出 {completion_delimiter}

######################
---示例---
######################
{examples}

#############################
---实际数据---
######################
实体类型: [{entity_types}]
文本: {input_text}
######################
注意:不能严格归类到给出实体类型的实体无需抽取
输出:"""

PROMPTS["entity_extraction_examples"] = [
    """示例1:

实体类型: ["矿物种类", "矿物特性", "地质作用", "化学成分", "矿物变化作用","物理化学条件"]

文本:
火山岩浆作用是岩浆作用的一种特殊形式。火山岩浆的成分同深成岩浆基本上相似，从超基性到酸性和碱性都有。
由于它侵入到地壳的最表层和突破岩层向地表喷溢，外部压力突然下降，使火山岩浆的冷却固结速度急剧加快，促使在高温低压条件下的特征矿物如 透长石、鳞石英等的形成。
同时火山岩浆作用所形成的矿物除斑晶外， 一般结晶细小，成隐晶质。

################
输出:
("entity"{tuple_delimiter}"透长石"{tuple_delimiter}"矿物种类"{tuple_delimiter}"是在火山岩浆作用过程中，因外部压力突然下降，冷却固结速度急剧加快，在高温低压条件下形成的特征矿物。"){record_delimiter}
("entity"{tuple_delimiter}"鳞石英"{tuple_delimiter}"矿物种类"{tuple_delimiter}"形成于火山岩浆作用，高温低压的特殊物理化学条件促使其产生，是该过程中的标志性矿物之一"){record_delimiter}
("entity"{tuple_delimiter}"结晶细小，成隐晶质"{tuple_delimiter}"矿物特性"{tuple_delimiter}"这是火山岩浆作用所形成矿物（除斑晶外）的显著特性。由于火山岩浆侵入到地壳最表层并向地表喷溢，外部压力骤降使得冷却固结速度加快，导致矿物结晶过程受到影响，呈现出结晶细小、多为隐晶质的特点。"){record_delimiter}
("entity"{tuple_delimiter}"火山岩浆作用"{tuple_delimiter}"地质作用"{tuple_delimiter}"作为岩浆作用的特殊形式，其岩浆成分与深成岩浆基本相似，涵盖从超基性到酸性和碱性的范围。过程中岩浆侵入地壳最表层甚至突破岩层喷溢至地表，压力和温度等物理化学条件的剧烈变化，引发了一系列矿物的形成和特性改变。"){record_delimiter}
("entity"{tuple_delimiter}"岩浆作用"{tuple_delimiter}"地质作用"{tuple_delimiter}"是一个宽泛概念，火山岩浆作用属于其中特殊的一种表现形式，它涉及岩浆从形成、运移到最终冷凝成岩的整个过程，对地壳物质组成和地质构造演化有着重要影响，火山岩浆作用就是在其大框架下因特殊环境而产生的独特地质现象。"){record_delimiter}
("entity"{tuple_delimiter}"高温低压"{tuple_delimiter}"物理化学条件"{tuple_delimiter}"火山岩浆作用的关键物理化学条件，在此条件下促使了如透长石、鳞石英等特征矿物的形成，同时也影响了矿物结晶特性，使其结晶细小、多为隐晶质。"){record_delimiter}
("relationship"{tuple_delimiter}"火山岩浆作用"{tuple_delimiter}"岩浆作用"{tuple_delimiter}"火山岩浆作用是岩浆作用的一种特殊形式。"{tuple_delimiter}"地质作用"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"透长石"{tuple_delimiter}"火山岩浆作用"{tuple_delimiter}"火山岩浆作用这种地质作用为透长石的形成提供了特定环境"{tuple_delimiter}"地质作用 形成条件"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"鳞石英"{tuple_delimiter}"火山岩浆作用"{tuple_delimiter}"火山岩浆作用这种地质作用为鳞石英的形成提供了特定环境"{tuple_delimiter}"地质作用 形成条件"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"透长石"{tuple_delimiter}"高温低压"{tuple_delimiter}"高温低压等物理化学条件促使了透长石的形成"{tuple_delimiter}"矿物形成的物理化学条件"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"鳞石英"{tuple_delimiter}"高温低压"{tuple_delimiter}"高温低压等物理化学条件促使了鳞石英的形成"{tuple_delimiter}"矿物形成的物理化学条件"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"结晶细小，成隐晶质"{tuple_delimiter}"火山岩浆作用"{tuple_delimiter}"火山岩浆作用过程中，由于岩浆侵入地壳表层及向地表喷溢的特殊情况，导致外部压力和冷却固结速度等条件变化，进而形成了矿物结晶细小、成隐晶质的特性，地质作用决定了矿物特性"{tuple_delimiter}"地质作用 矿物特性"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"透长石, 鳞石英, 结晶细小 成隐晶质, 火山岩浆作用, 岩浆作用, 高温低压"){completion_delimiter}
#############################""",
    """示例2:

实体类型: ["矿物种类", "矿物特性", "地质作用", "化学成分", "矿物变化作用","物理化学条件"]

文本:
赤铜矿 Cuprite KyipWT Cu₂O
〔化学组成〕 含Cu  88.82%。常含自然铜机械混合物。
〔晶体参数和结构〕等轴晶系；对称型432。空间群Pn3m;ao=4.26Å;Z=2。
氧离子位于单位晶胞的角顶和中心，铜离子配置于相互错开的1/8晶胞小立方体的四个中心。铜和氧的离子的配位数分别为2和4。
〔形态〕 单晶体呈八面体形，偶有呈八面体或立方体与菱形十二面体的聚形。有时呈针状或发状。集合体成致密粒状或土状。
〔物理性质〕 暗红色；条痕褐红；金刚光泽或半金属光泽；薄片微透明。硬度3.5~4.0;性脆；解理平行不完全。比重6.14。
〔成因和产状〕赤铜矿形成于外生条件，主要见于铜矿床的氧化带，系含铜硫化物氧化的产物。常与自然铜、孔雀石等伴生。
〔鉴定特征〕 金刚光泽，暗红色和褐红条痕色。
〔主要用途〕 大量产出时可作为提炼铜的矿物原料。


#############
输出:
("entity"{tuple_delimiter}"赤铜矿"{tuple_delimiter}"矿物种类"{tuple_delimiter}"赤铜矿是一种重要的铜矿石矿物，化学式为 “Cu₂O”。常含自然铜机械混合物，含铜量高达 88.82%，具有重要的经济价值，大量产出时可作为提炼铜的矿物原料。"){record_delimiter}
("entity"{tuple_delimiter}"含铜硫化物氧化"{tuple_delimiter}"矿物变化作用"{tuple_delimiter}"是赤铜矿形成的地质作用过程，通过含铜硫化物的氧化，促使赤铜矿的形成，使其成为铜矿床氧化带中的一种常见矿物。"){record_delimiter}
("entity"{tuple_delimiter}"金刚光泽，暗红色和褐红条痕色"{tuple_delimiter}"矿物特性"{tuple_delimiter}"是赤铜矿的鉴别特征"){record_delimiter}
("entity"{tuple_delimiter}"单晶体呈八面体形，偶有呈八面体或立方体与菱形十二面体的聚形。有时呈针状或发状。集合体成致密粒状或土状。"{tuple_delimiter}"矿物特性"{tuple_delimiter}"是赤铁矿的形态特征"){record_delimiter}
("entity"{tuple_delimiter}"Cu₂O"{tuple_delimiter}"化学成分"{tuple_delimiter}"是赤铜矿的主要化学成分"){record_delimiter}
("entity"{tuple_delimiter}"外生条件（赤铜矿形成的条件，见于铜矿床的氧化带）"{tuple_delimiter}"物理化学条件"{tuple_delimiter}"是赤铜矿的形成条件、成因"){record_delimiter}
("relationship"{tuple_delimiter}"赤铜矿"{tuple_delimiter}"含铜硫化物氧化"{tuple_delimiter}"赤铁矿是含铜硫化物氧化的产物"{tuple_delimiter}"形成条件"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"赤铜矿"{tuple_delimiter}"金刚光泽，暗红色和褐红条痕色"{tuple_delimiter}"赤铜矿的物理性质是金刚光泽，暗红色和褐红条痕色"{tuple_delimiter}"物理性质"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"赤铜矿"{tuple_delimiter}"单晶体呈八面体形，偶有呈八面体或立方体与菱形十二面体的聚形。有时呈针状或发状。集合体成致密粒状或土状。"{tuple_delimiter}"赤铜矿形态特征是单晶体呈八面体形，偶有呈八面体或立方体与菱形十二面体的聚形。有时呈针状或发状。集合体成致密粒状或土状。"{tuple_delimiter}"形态特征"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"赤铜矿"{tuple_delimiter}"Cu₂O"{tuple_delimiter}"赤铜矿主要化学成分是Cu₂O"{tuple_delimiter}"化学成分"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"赤铜矿"{tuple_delimiter}"外生条件（赤铜矿形成的条件，见于铜矿床的氧化带）"{tuple_delimiter}"赤铜矿的形成条件是外生条件"{tuple_delimiter}"形成条件"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"赤铜矿, 含铜硫化物氧化, Cu₂O, 外生条件"){completion_delimiter}
#############################"""

]

PROMPTS[
    "summarize_entity_descriptions"
] = """你是一个乐于助人的助手，负责对以下提供的数据生成全面的总结。
给定一到两个实体，以及一系列描述，所有这些描述都与同一个实体或一组实体相关。
请将所有这些内容连接成一个单一的、全面的描述。确保纳入从所有描述中收集到的信息。
如果所提供的描述相互矛盾，请解决这些矛盾并给出一个单一的、连贯的总结。
确保以第三人称进行书写，并包含实体名称，以便我们拥有完整的背景信息。
使用 {language} 作为输出语言.

#######
---Data---
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """如果仍有符合实体类型的实体未被提取，请使用相同的格式将他们添加到下面, 并补充相应relation数据
注意:不能严格归类到给出实体类型的实体无需抽取
实体类型:["矿物种类", "矿物特性", "地质作用", "化学成分", "矿物变化作用","物理化学条件"]
输出:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """似乎有些实体可能仍被遗漏了。如果仍有需要添加的实体，请回答 YES 或 NO 。
"""

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to user query about Knowledge Base provided below.


---Goal---

Generate a concise response based on Knowledge Base and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Knowledge Base, and incorporating general knowledge relevant to the Knowledge Base. Do not include information not provided by Knowledge Base.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Knowledge Base---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- If you don't know the answer, just say so.
- Do not make anything up. Do not include information not provided by the Knowledge Base."""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query and conversation history.

---Goal---

Given the query and conversation history, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Consider both the current query and relevant conversation history when extracting keywords
- Output the keywords in JSON format
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes
  - "low_level_keywords" for specific entities or details

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Conversation History:
{history}

Current Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Document Chunks provided below.

---Goal---

Generate a concise response based on Document Chunks and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Document Chunks, and incorporating general knowledge relevant to the Document Chunks. Do not include information not provided by Document Chunks.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Document Chunks---
{content_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- If you don't know the answer, just say so.
- Do not include information not provided by the Document Chunks."""


PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate whether these two questions are semantically similar, and whether the answer to Question 2 can be used to answer Question 1, provide a similarity score between 0 and 1 directly.

Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""

PROMPTS["mix_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Data Sources provided below.


---Goal---

Generate a concise response based on Data Sources and follow Response Rules, considering both the conversation history and the current query. Data sources contain two parts: Knowledge Graph(KG) and Document Chunks(DC). Summarize all information in the provided Data Sources, and incorporating general knowledge relevant to the Data Sources. Do not include information not provided by Data Sources.

When handling information with timestamps:
1. Each piece of information (both relationships and content) has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content/relationship and the timestamp
3. Don't automatically prefer the most recent information - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Data Sources---

1. From Knowledge Graph(KG):
{kg_context}

2. From Document Chunks(DC):
{vector_context}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- Organize answer in sesctions focusing on one main point or aspect of the answer
- Use clear and descriptive section titles that reflect the content
- List up to 5 most important reference sources at the end under "References" sesction. Clearly indicating whether each source is from Knowledge Graph (KG) or Vector Data (DC), in the following format: [KG/DC] Source content
- If you don't know the answer, just say so. Do not make anything up.
- Do not include information not provided by the Data Sources."""
