from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in one sentence, formatted as a JSON object with a sing"
)

formatted = prompt.format_messages(topic="quantum computing")
print(formatted)