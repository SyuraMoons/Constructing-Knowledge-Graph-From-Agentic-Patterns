"""LangGraph pattern: classifier"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("classifier_node", lambda x: x)
graph.set_entry_point("classifier_node")
graph.set_finish_point("classifier_node")
