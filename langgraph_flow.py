from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain.schema import SystemMessage
from langchain.chat_models import init_chat_model

from tools.action_execution import handle_utility_task
from tools.code_execution import handle_code_task


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def utility_tool(refined_input: str) -> str:
    """Handles app opening, Google or YouTube searches, and utility tasks."""
    return handle_utility_task(refined_input)


@tool
def code_tool(refined_input: str) -> str:
    """Handles code-related tasks like writing, reading, and structuring code."""
    return handle_code_task(refined_input)


llm = init_chat_model(model_provider="openai", model="gpt-4o-mini")

llm_with_tools = llm.bind_tools([utility_tool, code_tool])


def chatbot(state: State):
    system_prompt = SystemMessage(
        content="""
        You are a smart voice assistant. Classify the user's refined input into one of two types:
        1. Utility task: open apps, search Google/YouTube, or perform basic local actions.
        2. Code task: write, read, or structure code.

        Use the appropriate tool for the task and return the response.
        """
    )
    response = llm_with_tools.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}


tool_node = ToolNode(tools=[utility_tool, code_tool])

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


# def create_chat_graph(checkpointer=None):
#     return graph_builder.compile(checkpointer=checkpointer)
