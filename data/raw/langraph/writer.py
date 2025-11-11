"""LangGraph pattern: writer"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("writer_node", lambda x: x)
graph.set_entry_point("writer_node")
graph.set_finish_point("writer_node")
