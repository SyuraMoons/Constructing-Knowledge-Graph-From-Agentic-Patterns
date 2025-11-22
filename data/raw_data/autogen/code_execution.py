
"""AutoGen pattern: code_execution"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="code_execution_assistant",                   # Agent.name
    system_message="You are a helpful AI assistant for code_execution"  # Agent.systemMessage
)

user_proxy = UserProxyAgent(
    name="user",                                       # Agent.name
    human_input_mode="NEVER"                           # Agent.humanInputMode
)


