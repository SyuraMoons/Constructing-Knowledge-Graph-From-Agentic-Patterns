"""LangGraph pattern: executor"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("executor_node", lambda x: x)
graph.set_entry_point("executor_node")
graph.set_finish_point("executor_node")
