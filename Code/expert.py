# %%
import os
import backoff  # for exponential backoff

# data loader
from langchain.document_loaders.csv_loader import CSVLoader # 載入 CSV
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
# spliter
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
# embedding
from langchain.embeddings.openai import OpenAIEmbeddings
# vector DB
from langchain.vectorstores import Chroma, Pinecone
# LLM
from langchain.llms.fake import FakeListLLM # 測試用的
from langchain.llms import OpenAI # 比較舊的 model （text-davinci-003, text-davinci-002, davinci, curie, babbage, ada）
from langchain.chat_models import ChatOpenAI # 聊天式 model(比較近期的，例如：GPT-3.5-turbo, GPT-4) => 輸入需要 list of messages
# prompt
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ( # ChatOpenAI 所需的 templete 形式
  ChatPromptTemplate,
  SystemMessagePromptTemplate,
  HumanMessagePromptTemplate
)
# QA chain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler # 一邊生成一邊回答
# agent
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent

from langchain.output_parsers import StructuredOutputParser, ResponseSchema

import pandas as pd
import openai
import sys


print(os.getcwd())

# %%
# API Key 設置
import configparser
config = configparser.ConfigParser()
config.read('./Code/config.ini')
os.environ["OPENAI_API_KEY"] = config['OPEN_AI']['API_KEY']


# %%
# --------------------------------載入資料--------------------------------#
# loader = CSVLoader(file_path='./data/interview_clean.csv')
loader = DirectoryLoader('./data/expert_data/', glob='**/*.txt')
# 将数据转成 document 对象，每个文件会作为一个 document
documents = loader.load()
# 初始化加载器
# text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 300,
    chunk_overlap  = 30
)
# 切割加载的 document
split_docs = text_splitter.split_documents(documents)
split_docs

# %%
# --------------------------------轉為 embedding--------------------------------#
# 初始化 openai 的 embeddings 对象
embeddings = OpenAIEmbeddings(show_progress_bar=True)

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def get_embedding(**kwargs):
    docsearch = Chroma.from_documents(**kwargs)
    return docsearch
# docsearch = get_embedding(documents = split_docs, embedding = embeddings, persist_directory="./data/expert_embeddings/")
# 加载数据
docsearch = Chroma(persist_directory="./data/expert_embeddings/", embedding_function=embeddings)

# %%
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(model="gpt-3.5-turbo-16k-0613", temperature=0), chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True, verbose=True)

def Inference(question):
    result = qa({"query": question})
    articles = []
    for i in result['source_documents']:
        articles.append(i.page_content)
    return result, articles


# Inference(qa, "請問裕隆最近有什麼正向、負向討論？")

# %%
