"""LangGraph pattern: simple_graph"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("simple_graph_node", lambda x: x)
graph.set_entry_point("simple_graph_node")
graph.set_finish_point("simple_graph_node")
