import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from .tools import agent_tools

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))
llm_with_tools = llm.bind_tools(agent_tools)

def call_model(state: MessagesState):
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        sys_msg = SystemMessage(content="You are an AI assistant for a Healthcare Professional (HCP) CRM. You help sales representatives log interactions, edit logs, get HCP details, schedule follow-ups, and review past interactions. Be helpful, concise, and professional. Always use the available tools to fetch data or persist actions.")
        messages = [sys_msg] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(agent_tools)

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

graph_builder = StateGraph(MessagesState)

graph_builder.add_node("agent", call_model)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge("__start__", "agent")
graph_builder.add_conditional_edges("agent", should_continue, ["tools", END])
graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile()
