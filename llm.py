from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st

model_id = "openai/gpt-oss-120b"
access_token = "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"

llm_endpoint  = HuggingFaceEndpoint(
    repo_id=model_id,
    huggingfacehub_api_token=access_token
)

llmhg = ChatHuggingFace(llm=llm_endpoint)

st.title("BalaGPT")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

if prompt := st.chat_input("Prompt"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    res = llmhg.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=res.content))
    with st.chat_message("assistant"):
        st.markdown(res.content)


# st.write("Please enter your prompt")
# prompt = st.text_area("Prompt:", "")
# if st.button("Generate Response"):
#     if prompt.strip() == "":
#         st.error("Please enter your prompt first")
#     else:
#         response = llmhg.invoke(prompt)
#         text_output = response.content
#         st.success("Response Generated")
#         st.write(response.content)
