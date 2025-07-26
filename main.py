import os
import sys
from typing import Annotated

from typing_extensions import TypedDict

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY == '':
    print("A Gemini API KEY is required to start this chatbot")
    sys.exit(1)


llm = init_chat_model("google_genai:gemini-2.0-flash")


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}



graph_builder = StateGraph(State)
graph_builder.add_node('chatbot', chatbot)

# (ENTRY POINT TO THE CHATBOT): WHERE TO START EACH WORK EACH TIME IT RUN
graph_builder.add_edge(START, 'chatbot')

# (EXIT POINT TO THE CHATBOT): WHERE THE GRAPH SHOULD FINISH ITS EXECUTION
graph_builder.add_edge("chatbot", END)


graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


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
