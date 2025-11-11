"""LangGraph pattern: analyzer"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("analyzer_node", lambda x: x)
graph.set_entry_point("analyzer_node")
graph.set_finish_point("analyzer_node")
