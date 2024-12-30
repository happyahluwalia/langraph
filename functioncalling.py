from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage, AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated

messages = [AIMessage(content=f"Research about Astro Physics after High School", name="Model")]
messages.append(HumanMessage(content=f"How to apply for colleges that have major in Astro Physics", name="Student"))
messages.append(AIMessage(content=f"Here are some colleges that have major in Astro Physics", name="Model"))
messages.append(HumanMessage(content=f"Share with me profiles of successfully admitted students, things they have done in high school that made them stand out. dont need names of students etc, just things they did", name="Student"))

load_dotenv()

openapikey = os.environ.get("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", api_key=openapikey)
# result = llm.invoke(messages)

# new_message = HumanMessage(content="What is 2 multiplied by 3?", name="Student")    
# new_message1 = add_messages(messages, new_message)

# pprint(new_message1)    
def multiply(a: int, b: int) -> int:
    return a * b

def times(x: int, y: int) -> int:
    return x * y

llm_with_tools = llm.bind_tools([multiply, times])
# define Node
def tool_calling_llm_node(state:MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

#build a graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm_node", tool_calling_llm_node)
builder.add_edge(START, "tool_calling_llm_node")
builder.add_edge("tool_calling_llm_node", END)
graph = builder.compile()

messages = graph.invoke({"messages": HumanMessage(content="what is the answer if we add 3 to itself 4 times?", name="Student")})
for m in messages["messages"]:
    m.pretty_print()

    