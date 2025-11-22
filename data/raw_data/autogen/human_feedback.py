"""AutoGen pattern: human_feedback"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="human_feedback_assistant",
    system_message="You are a helpful AI assistant for human_feedback"
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)
