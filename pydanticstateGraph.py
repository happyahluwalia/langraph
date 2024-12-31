
import random
from regex import P
from pydanticstateschema import PydanticState
from langgraph.graph import StateGraph, START, END

def node_1(state: PydanticState):
    print("Node 1")
    return {"name": state.name + " is .... "}

def node_2(state: PydanticState):
    print("Node 2")
    return {"mood": state.mood }

def node_3(state: PydanticState):
    print("Node 3")
    return {"mood": state.mood }

def decide_mood(state: PydanticState):
    print("Decide mood")
    if state.mood == 'happy':
        return "node_2"
   
    return "node_3"
    

builder = StateGraph(PydanticState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

graph.invoke(PydanticState(name="John", mood="happy"))
