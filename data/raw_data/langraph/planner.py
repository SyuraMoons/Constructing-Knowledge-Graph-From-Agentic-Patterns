"""LangGraph pattern: planner"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("planner_node", lambda x: x)
graph.set_entry_point("planner_node")
graph.set_finish_point("planner_node")
