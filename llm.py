from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import streamlit as st

model_id = "openai/gpt-oss-120b"
access_token = "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"

llm_endpoint  = HuggingFaceEndpoint(
    repo_id=model_id,
    huggingfacehub_api_token=access_token
)

llmhg = ChatHuggingFace(llm=llm_endpoint)

st.title("BalaGPT")
st.write("Please enter your prompt")
prompt = st.text_area("Prompt:", "")
if st.button("Generate Response"):
    if prompt.strip() == "":
        st.error("Please enter your prompt first")
    else:
        response = llmhg.invoke(prompt)
        text_output = response.content
        st.success("Response Generated")
        st.write(response.content)

# formatted = text_output.replace("\n", " ")
# print(formatted)