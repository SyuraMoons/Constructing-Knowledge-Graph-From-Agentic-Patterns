"""LangGraph pattern: synthesizer"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("synthesizer_node", lambda x: x)
graph.set_entry_point("synthesizer_node")
graph.set_finish_point("synthesizer_node")
