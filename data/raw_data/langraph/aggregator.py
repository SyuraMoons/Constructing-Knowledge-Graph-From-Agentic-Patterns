"""LangGraph pattern: aggregator"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("aggregator_node", lambda x: x)
graph.set_entry_point("aggregator_node")
graph.set_finish_point("aggregator_node")
