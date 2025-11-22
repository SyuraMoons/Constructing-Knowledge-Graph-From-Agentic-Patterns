"""CrewAI pattern: starter_template"""
from crewai import Agent, Crew, Task

class StarterCrew:
    def assistant_agent(self):
        return Agent(
            role="AI Assistant",
            goal="Help users accomplish tasks efficiently",
            backstory="You are a helpful AI assistant with broad knowledge",
            verbose=True
        )

    def main_task(self):
        return Task(
            description="Complete the user's request: {user_request}",
            expected_output="Task completion summary and results",
            agent=self.assistant_agent()
        )

    def crew(self):
        return Crew(
            agents=[self.assistant_agent()],
            tasks=[self.main_task()],
            verbose=True,
            process="sequential"
        )

def main():
    crew = StarterCrew()
    result = crew.crew().kickoff(inputs={"user_request": "Your task here"})
    print(result)

if __name__ == "__main__":
    main()
