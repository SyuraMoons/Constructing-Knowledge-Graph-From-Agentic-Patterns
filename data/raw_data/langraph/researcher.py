"""LangGraph pattern: researcher"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("researcher_node", lambda x: x)
graph.set_entry_point("researcher_node")
graph.set_finish_point("researcher_node")
