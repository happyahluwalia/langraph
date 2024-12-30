# This is an Agent with memory using the ReACT pattern
# The smart thing is that the add method takes 2 int values, but we pass a float. The LLM looks at the error, rounds up the int, and then adds the numbers
# Mind-blowing!

import dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition 
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from utils import multiply, add, divide

# Load environment variables from .env file
dotenv.load_dotenv()

# Create a ChatOpenAI model with the gpt-4o model
llm = ChatOpenAI(model="gpt-4o")

# Define the tools to be used
tools = [multiply, add, divide]

# Bind the tools to the ChatOpenAI model
llm_tools = llm.bind_tools(tools)

# Define the memory saver
memory = MemorySaver()

# Define the configuration
config = {"configurable":{"thread_id": 1}}

# Define the assistant node
def assistant(state: MessagesState):
    # Call the ChatOpenAI model with the input messages
    sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.  Fix any errors if you see any ")
    return {"messages": [llm_tools.invoke([sys_msg] + state["messages"])]}

# Build the graph
builder = StateGraph(MessagesState)

# Add nodes to the graph
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Link the nodes using edges
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

# Compile the graph
graph = builder.compile(checkpointer=memory)

# Define the messages to be processed
messages = [HumanMessage(content="Add 3 and 4. Multiply the output by 2. Divide the output by 5")]

# Process the messages
messages = graph.invoke({"messages": messages}, config)

# Now add float to int which will error out and model will fix it due to ReACT pattern
messages = [HumanMessage(content="Add 5 to it")]

# Process the messages
messages = graph.invoke({"messages": messages}, config)

# Print the results
for m in messages["messages"]:
    m.pretty_print()
