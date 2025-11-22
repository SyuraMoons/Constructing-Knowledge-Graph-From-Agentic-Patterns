"""LangGraph pattern: supervisor"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("supervisor_node", lambda x: x)
graph.set_entry_point("supervisor_node")
graph.set_finish_point("supervisor_node")
