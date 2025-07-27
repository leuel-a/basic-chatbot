#!/usr/bin/env python3
import os
import sys
from typing import Annotated
from typing_extensions import TypedDict

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

from utils import _set_env

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
if GOOGLE_API_KEY == '':
    print("A GOOGLE API KEY is required to start this chatbot")
    sys.exit(1)


_set_env("GOOGLE_API_KEY")
_set_env("TAVILY_API_KEY")

search_tool = TavilySearch(max_results=2)
tools = [search_tool]

llm = init_chat_model("google_genai:gemini-2.0-flash")
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def route_tools(state: State):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = list(state)[-1]
    elif messages := state.get('messages', ''):
        ai_message = messages[-1]
    else:
        raise ValueError(f'No messages found in input state to tool_edge: {state}')
    
    if hasattr(ai_message, "tool_calls") and len(getattr(ai_message , "tool_calls")) > 0:
        return "tools"
    return END


tool_node = ToolNode(tools=[search_tool])

memory = InMemorySaver()

graph_builder = StateGraph(State)
graph_builder.add_node('chatbot', chatbot)
graph_builder.add_node('tools', tool_node)

# (ENTRY POINT TO THE CHATBOT): WHERE TO START EACH WORK EACH TIME IT RUN
graph_builder.add_edge(START, 'chatbot')

# (EXIT POINT TO THE CHATBOT): WHERE THE GRAPH SHOULD FINISH ITS EXECUTION
graph_builder.add_edge("chatbot", END)

graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition
    )

graph = graph_builder.compile(checkpointer=memory)

config: RunnableConfig = {'configurable': {'thread_id': '1'}}

def stream_graph_updates(user_input: str):
    events = graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config,
            stream_mode="values"
        )
    for event in events:
        event["messages"][-1].pretty_print()


## FOR VISUALIZATION
display(Image(graph.get_graph().draw_mermaid_png()))

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
