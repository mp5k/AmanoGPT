from langchain.chat_models import ChatOpenAI
import os
from langchain.schema import (
    SystemMessage,  # システムメッセージ
    HumanMessage,  # 人間の質問
    AIMessage  # ChatGPTの返答
)

variable = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI()  # ChatGPT APIを呼んでくれる機能
message = "Hi, ChatGPT!"  # あなたの質問をここに書く

messages = [
    SystemMessage(content="絶対に関西弁で返答してください"),
    HumanMessage(content=message)
]
response = llm(messages)
print(response)

# content='Hello! How can I assist you today?' additional_kwargs={} example=False