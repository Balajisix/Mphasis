import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

model_id = os.getenv("HF_MODEL")
access_token = os.getenv("HF_TOKEN")

# it's like a engine we communicate
llm_endpoint  = HuggingFaceEndpoint(
    repo_id=model_id,
    huggingfacehub_api_token=access_token
)

# it's a chat wrapper
llmhg = ChatHuggingFace(llm=llm_endpoint)

messages = []
messages.append(SystemMessage(content="Please refine the answer according to examples given"))
messages.append(HumanMessage(content="What is spoken in France?"))
messages.append(AIMessage(content="French haha hehe hoho"))
messages.append(HumanMessage(content="What is spoken in Italy?"))
messages.append(AIMessage(content="Italian haha hehe hoho"))
messages.append(HumanMessage(content="What is spoken in China?"))
messages.append(AIMessage(content="Chinese haha hehe hoho"))

messages.append(HumanMessage(content="What is spoken in Germany?"))

res = llmhg.invoke(messages)

print(res.content)