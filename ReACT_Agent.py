# This file is a simple example of how to use the langgraph library to build a graph that calls a tool from langchain_openai
import dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition 
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from utils import multiply, add, divide

dotenv.load_dotenv()  # Load environment variables from .env file

llm = ChatOpenAI(model="gpt-4o")  # Create a ChatOpenAI model with the gpt-4o model
tools = [multiply, add, divide]
llm_tools = llm.bind_tools(tools)  # Bind the multiply function to the ChatOpenAI model

# Node definition
def assistant(state: MessagesState):
    # Call the ChatOpenAI model with the input messages
    sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.  ")
    return {"messages": [llm_tools.invoke([sys_msg] + state["messages"])]}
    # System message

    # return {"messages": [llm_tools.invoke([sys_msg] + [m]) for m in state["messages"]]}


# Building the graph
builder = StateGraph(MessagesState)  # Create a StateGraph with the MessagesState
# Add nodes
builder.add_node("assistant", assistant)  # Add a node that calls the ChatOpenAI model
builder.add_node("tools", ToolNode(tools))  # Add a node that contains the multiply tool

# link using edges
builder.add_edge(START, "assistant")  # Add an edge from the start node to the tool_calling_llm node
builder.add_conditional_edges("assistant", tools_condition)  # Add conditional edges to the tool_calling_llm node
builder.add_edge("tools","assistant")  # Add an edge from the tool_calling_llm node to the end node

graph = builder.compile()  # Compile the graph

# messages = [HumanMessage(content="This is a test run to check what is 2 when added three times to itself and then divide the answer by 2 and add 4 to it.")]  # Create a list of messages
messages = [HumanMessage(content="Add 3 and 4. Multiply the output by 2. Divide the output by 5")]  # Create a list of messages
#messages.append(HumanMessage(content="This is a test run to check what is 2 times 3"))  # Create a list of messages
messages = graph.invoke({"messages": messages})  # Invoke the graph with the messages
for m in messages["messages"]:
    m.pretty_print()  # Print the results