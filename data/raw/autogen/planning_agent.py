"""AutoGen pattern: planning_agent"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="planning_agent_assistant",
    system_message="You are a helpful AI assistant for planning_agent"
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)
