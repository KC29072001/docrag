from langchain_core.prompts import PromptTemplate

rewrite_prompt = """
Look at the input and try to reason about the underlying semantic intent / meaning.
Here is the initial question:
-------
{question}
-------
Formulate an improved question:
"""