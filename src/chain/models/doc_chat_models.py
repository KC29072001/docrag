from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.pydantic_v1 import BaseModel, Field

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

class Grade(BaseModel):
    binary_score: str = Field(description="Relevance score 'yes' or 'no'")