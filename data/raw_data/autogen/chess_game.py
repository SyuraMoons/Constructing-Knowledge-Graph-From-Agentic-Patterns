"""AutoGen pattern: chess_game"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="chess_game_assistant",                      # Agent.name
    system_message="You are a helpful AI assistant for chess_game"  # Agent.systemMessage
)

user_proxy = UserProxyAgent(
    name="user",                                      # Agent.name
    human_input_mode="NEVER"                          # Agent.humanInputMode
)


