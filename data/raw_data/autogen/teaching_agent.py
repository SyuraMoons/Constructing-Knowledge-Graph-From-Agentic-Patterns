"""AutoGen pattern: teaching_agent"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="teaching_agent_assistant",
    system_message="You are a helpful AI assistant for teaching_agent"
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)
