# This file is a simple example of how to use the langgraph library to build a graph that calls a tool from langchain_openai
import dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition 
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    # Simple multiplication function
    return a * b

dotenv.load_dotenv()  # Load environment variables from .env file

llm = ChatOpenAI(model="gpt-4o")  # Create a ChatOpenAI model with the gpt-4o model
llm_tools = llm.bind_tools([multiply])  # Bind the multiply function to the ChatOpenAI model

# Node definition
def tool_calling_llm(state: MessagesState):
    # Call the ChatOpenAI model with the input messages
    # return {"messages": [llm_tools.invoke(state["messages"])]}
    return {"messages": [llm_tools.invoke([m]) for m in state["messages"]]}


# Building the graph
builder = StateGraph(MessagesState)  # Create a StateGraph with the MessagesState
builder.add_node("tool_calling_llm", tool_calling_llm)  # Add a node that calls the ChatOpenAI model
builder.add_node("tools", ToolNode([multiply]))  # Add a node that contains the multiply tool
builder.add_edge(START, "tool_calling_llm")  # Add an edge from the start node to the tool_calling_llm node
builder.add_conditional_edges("tool_calling_llm", tools_condition)  # Add conditional edges to the tool_calling_llm node
builder.add_edge("tool_calling_llm", END)  # Add an edge from the tool_calling_llm node to the end node

graph = builder.compile()  # Compile the graph

messages = [HumanMessage(content="This is a test run to check what is 2 when added three times to itself")]  # Create a list of messages
messages.append(HumanMessage(content="This is a test run to check what is 2 times 3"))  # Create a list of messages
messages = graph.invoke({"messages": messages})  # Invoke the graph with the messages
for m in messages["messages"]:
    m.pretty_print()  # Print the results