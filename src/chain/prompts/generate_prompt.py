from langchain_core.prompts import PromptTemplate

generate_prompt = PromptTemplate.from_template("""
You are an AI assistant tasked with answering questions based on the provided context. Use the following pieces of context to answer the question at the end. Answer these questions in a very detailed manner. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}
""")