from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

model_id = os.getenv("HF_MODEL")
access_token = os.getenv("HF_TOKEN")

llm_endpoint = HuggingFaceEndpoint(
    repo_id=model_id,
    huggingfacehub_api_token=access_token
)
llmhg = ChatHuggingFace(llm=llm_endpoint)

if "store" not in st.session_state:
    st.session_state.store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = InMemoryChatMessageHistory()
    return st.session_state.store[session_id]

with_message_history = RunnableWithMessageHistory(
    llmhg,
    get_session_history,
)

st.title("BalaGPT")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Prompt"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    session_id = "balaji2003"
    config = {"configurable": {"session_id": session_id}}

    res = with_message_history.invoke(
        [HumanMessage(content=prompt)],
        config=config
    )

    ai_content = None
    if hasattr(res, "content"):
        ai_content = res.content
    elif isinstance(res, (list, tuple)) and len(res) > 0 and hasattr(res[0], "content"):
        ai_content = res[0].content
    else:
        ai_content = str(res)

    st.session_state.messages.append({"role": "assistant", "content": ai_content})
    with st.chat_message("assistant"):
        st.markdown(ai_content)