"""AutoGen pattern: web_search"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="web_search_assistant",
    system_message="You are a helpful AI assistant for web_search"
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)
