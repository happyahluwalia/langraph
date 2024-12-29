from typing_extensions import TypedDict
import random
from typing import Literal 
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    graph_state: str
    
def Node_1(state: State):
    print('Node_1')
    state['graph_state'] += ' Node_1'

def Node_2(state: State):
    print('Node_2')
    state['graph_state'] += ' Node_2'

def Node_3(state: State):
    print('Node_3')
    state['graph_state'] += ' Node_3'

def decide_node(state: State)-> Literal['node_2', 'node_3']:
    """
        Deciding function on which node to go next
    """
    print('decide_node')
    user_input = state['graph_state']
    if random.random() < 0.5:
        return 'node_2'
    else:
        return 'node_3'
    
# Graph construction
builder = StateGraph(State)
builder.add_node("node_1", Node_1)
builder.add_node("node_2", Node_2)
builder.add_node("node_3", Node_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_node)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

# graph invocation
graph.invoke({'graph_state': 'Where am I?'})
