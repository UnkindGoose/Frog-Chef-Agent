import re
from langdetect import detect
from typing import TypedDict, Optional, List, Annotated

from langchain_core.messages import AnyMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from utils.models import *


'''
Declaring Agent State
'''

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    language: str
    image: Optional[str]
    

'''
Nodes and routers
'''

def translation_router(state: AgentState):
    
    print("--Deciding translation\n")
    
    if state['language'] != detect(state['messages'][-1].content):
        return 'translate'
    else:
        return 'next'


def meal_router(state: AgentState):
    
    print("--Deciding meal recipe\n")
    
    last_msg = state["messages"][-1]
    if last_msg.tool_calls and isinstance(last_msg, AIMessage):
        return "tools"
    return "end"


def llm_node(state: AgentState):
    
    print("--Entering LLM Node\n")
    
    llm_chain = llm_chain_proxy
    response = llm_chain.invoke({'input':state['messages']})
    response.content = re.sub(r"<think>.*?</think>", "", response.content, flags=re.DOTALL).strip()
    
    return {'messages': [response]}


def translate_node(state: AgentState):
    
    print("--Entering Translation Node\n")
    
    translation_chain = translation_chain_proxy
    translation = translation_chain.invoke({'input':state['messages'][-1].content})
    
    return {'messages': [translation]}

'''
Describing the resulting graph
'''

builder = StateGraph(AgentState)


find_meal_node = ToolNode([find_closest_meal], messages_key="messages")


builder.add_node("translation_router", lambda state: state)
builder.add_node("translator", translate_node)
builder.add_node("llm", llm_node)
builder.add_node("find_meal", find_meal_node)


builder.add_edge(START, 'llm')
builder.add_conditional_edges("llm", meal_router, {"tools": "find_meal", "end": 'translation_router'})
builder.add_conditional_edges("translation_router", translation_router, {'translate':'translator', 'next':END})
builder.add_edge("translator", END)
builder.add_edge("find_meal", "llm")


graph = builder.compile()


__all__=['graph']