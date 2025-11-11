"""AutoGen pattern: function_calling"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="function_calling_assistant",
    system_message="You are a helpful AI assistant for function_calling"
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)
