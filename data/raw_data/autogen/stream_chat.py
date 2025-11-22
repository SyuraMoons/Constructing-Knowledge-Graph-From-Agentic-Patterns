"""AutoGen pattern: stream_chat"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="stream_chat_assistant",
    system_message="You are a helpful AI assistant for stream_chat"
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)
