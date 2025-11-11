"""AutoGen pattern: chess_game"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="chess_game_assistant",
    system_message="You are a helpful AI assistant for chess_game"
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)
