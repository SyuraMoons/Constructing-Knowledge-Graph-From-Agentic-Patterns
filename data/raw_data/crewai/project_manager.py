from crewai import Agent, Task

agent = Agent(role="Researcher",goal="Summarize research papers"   )
task = Task(description="Collect papers from arXiv"  )
agent.performsTask = task
task.hasAssignedAgent = agent
