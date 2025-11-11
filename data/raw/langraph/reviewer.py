"""LangGraph pattern: reviewer"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("reviewer_node", lambda x: x)
graph.set_entry_point("reviewer_node")
graph.set_finish_point("reviewer_node")
