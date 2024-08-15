# from langgraph.graph import END, StateGraph
# from langgraph.prebuilt import ToolNode, tools_condition
# from src.chain.agents.doc_chat_agent import agent, grade_documents, rewrite, generate
# from src.chain.models.doc_chat_models import AgentState

# def create_doc_chat_graph(tools):
#     workflow = StateGraph(AgentState)
#     workflow.add_node("agent", agent)
#     retrieve = ToolNode(tools)
#     workflow.add_node("retrieve", retrieve)
#     workflow.add_node("rewrite", rewrite)
#     workflow.add_node("generate", generate)
#     workflow.set_entry_point("agent")
#     workflow.add_conditional_edges("agent", tools_condition, {"tools": "retrieve", END: END})
#     workflow.add_conditional_edges("retrieve", grade_documents)
#     workflow.add_edge("generate", END)
#     workflow.add_edge("rewrite", "agent")
#     return workflow.compile()




# faiss
# from langgraph.graph import END, StateGraph
# from langgraph.prebuilt import ToolNode, tools_condition
# from src.chain.agents.doc_chat_agent import agent, grade_documents, rewrite, generate
# from src.chain.models.doc_chat_models import AgentState

# def create_doc_chat_graph(tools):
#     workflow = StateGraph(AgentState)
    
#     # Pass tools to the agent function
#     workflow.add_node("agent", lambda state: agent(state, tools))
    
#     retrieve = ToolNode(tools)
#     workflow.add_node("retrieve", retrieve)
#     workflow.add_node("rewrite", rewrite)
#     workflow.add_node("generate", generate)
#     workflow.set_entry_point("agent")
#     workflow.add_conditional_edges("agent", tools_condition, {"tools": "retrieve", END: END})
#     workflow.add_conditional_edges("retrieve", grade_documents)
#     workflow.add_edge("generate", END)
#     workflow.add_edge("rewrite", "agent")
#     return workflow.compile()


# /chat fix 
# src/chain/agentgraph/doc_chat.py

# from langgraph.graph import END, StateGraph
# from langgraph.prebuilt import ToolNode, tools_condition
# from src.chain.agents.doc_chat_agent import agent, grade_documents, rewrite, generate
# from src.chain.models.doc_chat_models import AgentState

# def create_doc_chat_graph(tools):
#     workflow = StateGraph(AgentState)
#     workflow.add_node("agent", agent)
#     retrieve = ToolNode(tools)
#     workflow.add_node("retrieve", retrieve)
#     workflow.add_node("rewrite", rewrite)
#     workflow.add_node("generate", generate)
#     workflow.set_entry_point("agent")
#     workflow.add_conditional_edges("agent", tools_condition, {"tools": "retrieve", END: END})
#     workflow.add_conditional_edges("retrieve", grade_documents)
#     workflow.add_edge("generate", END)
#     workflow.add_edge("rewrite", "agent")
#     return workflow.compile()




# src/chain/agentgraph/doc_chat.py

from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from src.chain.agents.doc_chat_agent import agent, grade_documents, rewrite, generate
from src.chain.models.doc_chat_models import AgentState

def create_doc_chat_graph(tools):
    workflow = StateGraph(AgentState)
    
    # Modify the agent node to include tools
    workflow.add_node("agent", lambda state: agent(state, tools))
    
    retrieve = ToolNode(tools)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("rewrite", rewrite)
    workflow.add_node("generate", generate)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", tools_condition, {"tools": "retrieve", END: END})
    workflow.add_conditional_edges("retrieve", grade_documents)
    workflow.add_edge("generate", END)
    workflow.add_edge("rewrite", "agent")
    return workflow.compile()