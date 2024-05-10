import os
import nonebot
from nonebot import on_message
from nonebot.plugin import export
from nonebot.plugin import require as pluginR
from nonebot.adapters.cqhttp import Event, Bot, Message
from nonebot.log import logger
from nonebot.rule import to_me

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
import weaviate
from weaviate.embedded import EmbeddedOptions
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_community.vectorstores import Weaviate
import requests

config = nonebot.get_driver().config

tool = pluginR('tool')
group_ids = tool.group_ids

util = pluginR('util')

path = os.path.abspath(os.path.dirname(__file__))

# 加载数据
loader = TextLoader(path + '/eveonline-ai.txt')
documents = loader.load()
# 文本分块
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)
# 初始化向量数据库并嵌入目标文档
client = weaviate.Client(
    embedded_options=EmbeddedOptions()
)
vectorstore = Weaviate.from_documents(
    client=client,
    documents=chunks,
    embedding=OllamaEmbeddings(model="llama2-chinese:7b-chat"),
    by_text=False
)
# 检索器
retriever = vectorstore.as_retriever()
# LLM 提示模板
template = """
你是 EVE Online 小精灵，为玩家提供帮助，使用以下检索到的上下文片段来回答问题。如果你不知道答案，只需说你不知道。
最多使用三句话，保持回答简洁。
问题：{question}
上下文：{context}
答案：
"""
prompt = ChatPromptTemplate.from_template(template)
llm = ChatOllama(model="llama2-chinese:7b-chat", temperature=6)
rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)

# 查询&生成
# print(rag_chain.invoke("氧的ID是什么？"))

ai = on_message(rule=to_me())
@ai.handle()
async def _(bot: Bot, event: Event):
    global content

    if not (event.message_type == 'group' and event.group_id in group_ids) :
        return
    if await util.isPass() or await util.isBan(event.user_id) :
        return

    msg = rag_chain.invoke(str(event.get_message()))

    await ai.finish(message=Message(msg))
