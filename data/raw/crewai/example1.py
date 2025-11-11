from crewai import Agent, Task

agent = Agent(role="Researcher", goal="Summarize research papers")
task = Task(description="Collect papers from arXiv")
