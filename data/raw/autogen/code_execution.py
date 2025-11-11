"""AutoGen pattern: code_execution"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="code_execution_assistant",
    system_message="You are a helpful AI assistant for code_execution"
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)
