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

if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = None

if "session_id_input" not in st.session_state:
    st.session_state.session_id_input = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = InMemoryChatMessageHistory()
    return st.session_state.store[session_id]

with_message_history = RunnableWithMessageHistory(
    llmhg,
    get_session_history,
)

st.title("Generative AI Class")

st.markdown("**Session controls**")
st.text_input("Enter session id", key="session_id_input", help="Type a session id and click Use Session")
col1, col2 = st.columns([1,1])
with col1:
    if st.button("Use Session"):
        sid = st.session_state.session_id_input.strip()
        if sid == "":
            st.warning("Please enter a non-empty session id")
        else:
            st.session_state.active_session_id = sid
            hist = get_session_history(sid)
            st.session_state.messages = []
            for m in hist.messages:
                role = "user" if getattr(m, "type", None) == "human" else "assistant"
                st.session_state.messages.append({"role": role, "content": getattr(m, "content", str(m))})
            st.success(f"Switched to session {sid}")
with col2:
    if st.button("Clear UI Messages"):
        st.session_state.messages = []

if st.button("Delete Stored History for Active Session"):
    sid = st.session_state.active_session_id
    if sid and sid in st.session_state.store:
        del st.session_state.store[sid]
        st.session_state.messages = []
        st.success(f"Deleted history for session {sid}")
    else:
        st.info("No active session or no stored history to delete")

st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Prompt"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    session_id = st.session_state.active_session_id or st.session_state.session_id_input or "default"
    config = {"configurable": {"session_id": session_id}}

    try:
        res = with_message_history.invoke(
            [HumanMessage(content=prompt)],
            config=config
        )
    except Exception as e:
        st.error(f"LLM call failed: {e}")
    else:
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
