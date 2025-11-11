"""AutoGen pattern: feedback_agent"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="feedback_agent_assistant",
    system_message="You are a helpful AI assistant for feedback_agent"
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)
