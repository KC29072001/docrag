from langchain.tools.retriever import create_retriever_tool

def create_retriever_tools(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return [create_retriever_tool(
        retriever,
        "retrieve_documents",
        "Search and retrieve information from the loaded documents."
    )]