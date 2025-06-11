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
    """Handles app opening, URL launching, Google/YouTube searching, or basic utility actions on the local system."""
    return handle_utility_task(refined_input)


@tool
def code_tool(refined_input: str) -> str:
    """Handles programming-related tasks like writing, reading, refactoring, or explaining code."""
    return handle_code_task(refined_input)


llm = init_chat_model(model_provider="openai", model="gpt-4o-mini")

llm_with_tools = llm.bind_tools([utility_tool, code_tool])


def chatbot(state: State):
    system_prompt = SystemMessage(
        content="""
        You are a smart voice assistant. You must classify the user's refined input into one of two types:

        1. Utility task:
        - Includes requests to open applications, websites, perform Google or YouTube searches, or launch system utilities.
        - Examples: "Open YouTube", "Search for cats on Google", "Launch calculator".

        2. Code task:
        - Includes requests to generate, read, or structure programming code.
        - Examples: "Write a Python function", "Read my JavaScript file", "Refactor this code".

        You MUST choose the correct tool and call it directly. DO NOT generate a text reply yourself unless explicitly asked.

        Return only the tool output.
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
