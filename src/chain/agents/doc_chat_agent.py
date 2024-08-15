# from langchain_groq import ChatGroq
# from langchain_core.output_parsers import StrOutputParser
# from src.chain.config.settings import GROQ_API_KEY
# from src.chain.prompts.doc_chat_prompts import relevance_prompt, rewrite_prompt, generate_prompt
# from src.chain.models.doc_chat_models import Grade

# def grade_documents(state):
#     print("---CHECK RELEVANCE---")
#     llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
#     llm_with_tool = llm.with_structured_output(Grade)
#     chain = relevance_prompt | llm_with_tool
#     messages = state["messages"]
#     question = messages[0].content
#     docs = messages[-1].content
#     scored_result = chain.invoke({"question": question, "context": docs})
#     score = scored_result.binary_score
#     if score == "yes":
#         print("---DECISION: DOCS RELEVANT---")
#         return "generate"
#     else:
#         print("---DECISION: DOCS NOT RELEVANT---")
#         print(score)
#         return "rewrite"

# def agent(state):
#     print("---CALL AGENT---")
#     messages = state["messages"]
#     model = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
#     model = model.bind_tools(tools)
#     response = model.invoke(messages)
#     return {"messages": [response]}

# def rewrite(state):
#     print("---TRANSFORM QUERY---")
#     messages = state["messages"]
#     question = messages[0].content
#     model = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
#     response = model.invoke([{"role": "human", "content": rewrite_prompt.format(question=question)}])
#     return {"messages": [response]}

# def generate(state):
#     print("---GENERATE---")
#     messages = state["messages"]
#     question = messages[0].content
#     docs = messages[-1].content
#     llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
#     rag_chain = generate_prompt | llm | StrOutputParser()
#     response = rag_chain.invoke({"context": docs, "question": question})
#     return {"messages": [response]}







# from langchain_groq import ChatGroq
# from langchain_core.output_parsers import StrOutputParser
# from src.chain.config.settings import GROQ_API_KEY
# from src.chain.prompts.doc_chat_prompts import relevance_prompt, rewrite_prompt, generate_prompt
# from src.chain.models.doc_chat_models import Grade

# def grade_documents(state):
#     print("---CHECK RELEVANCE---")
#     llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
#     llm_with_tool = llm.with_structured_output(Grade)
#     chain = relevance_prompt | llm_with_tool
#     messages = state["messages"]
#     question = messages[0].content
#     docs = messages[-1].content
#     scored_result = chain.invoke({"question": question, "context": docs})
#     score = scored_result.binary_score
#     if score == "yes":
#         print("---DECISION: DOCS RELEVANT---")
#         return "generate"
#     else:
#         print("---DECISION: DOCS NOT RELEVANT---")
#         print(score)
#         return "rewrite"

# def agent(state, tools):
#     print("---CALL AGENT---")
#     messages = state["messages"]
#     model = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
#     model = model.bind_tools(tools)
#     response = model.invoke(messages)
#     return {"messages": [response]}

# def rewrite(state):
#     print("---TRANSFORM QUERY---")
#     messages = state["messages"]
#     question = messages[0].content
#     model = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
#     response = model.invoke([{"role": "human", "content": rewrite_prompt.format(question=question)}])
#     return {"messages": [response]}

# def generate(state):
#     print("---GENERATE---")
#     messages = state["messages"]
#     question = messages[0].content
#     docs = messages[-1].content
#     llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
#     rag_chain = generate_prompt | llm | StrOutputParser()
#     response = rag_chain.invoke({"context": docs, "question": question})
#     return {"messages": [response]}





import logging
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from src.chain.config.settings import GROQ_API_KEY
from src.chain.prompts.relevance_prompt import relevance_prompt
from src.chain.prompts.generate_prompt import generate_prompt
from src.chain.prompts.rewrite_prompt import rewrite_prompt
from src.chain.prompts.doc_chat_prompts import relevance_prompt, rewrite_prompt, generate_prompt
from src.chain.models.doc_chat_models import Grade


logger = logging.getLogger(__name__)

def agent(state, tools):
    logger.info("---CALL AGENT---")
    messages = state["messages"]
    model = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    return {"messages": messages + [response]}

def grade_documents(state):
    logger.info("---CHECK RELEVANCE---")
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
    llm_with_tool = llm.with_structured_output(Grade)
    chain = relevance_prompt | llm_with_tool
    messages = state["messages"]
    question = messages[0].content
    docs = messages[-1].content
    scored_result = chain.invoke({"question": question, "context": docs})
    score = scored_result.binary_score
    if score == "yes":
        logger.info("---DECISION: DOCS RELEVANT---")
        return "generate"
    else:
        logger.info("---DECISION: DOCS NOT RELEVANT---")
        logger.info(score)
        return "rewrite"

def rewrite(state):
    logger.info("---TRANSFORM QUERY---")
    messages = state["messages"]
    question = messages[0].content
    model = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
    response = model.invoke([{"role": "human", "content": rewrite_prompt.format(question=question)}])
    return {"messages": messages + [response]}

def generate(state):
    logger.info("---GENERATE---")
    messages = state["messages"]
    question = messages[0].content
    docs = messages[-1].content
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0)
    rag_chain = generate_prompt | llm | StrOutputParser()
    response = rag_chain.invoke({"context": docs, "question": question})
    return {"messages": messages + [{"role": "assistant", "content": response}]}