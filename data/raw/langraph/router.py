"""LangGraph pattern: router"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("router_node", lambda x: x)
graph.set_entry_point("router_node")
graph.set_finish_point("router_node")
