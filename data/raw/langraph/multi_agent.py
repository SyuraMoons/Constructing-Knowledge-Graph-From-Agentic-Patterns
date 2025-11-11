"""LangGraph pattern: multi_agent"""
from langgraph.graph import StateGraph

# Define graph
graph = StateGraph()
graph.add_node("multi_agent_node", lambda x: x)
graph.set_entry_point("multi_agent_node")
graph.set_finish_point("multi_agent_node")
