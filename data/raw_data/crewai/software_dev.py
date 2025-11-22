"""CrewAI pattern: game_builder"""
from crewai import Agent, Crew, Task
from crewai_tools import CodeExecutionTool, PythonREPL
from pydantic import BaseModel

class GameDesign(BaseModel):
    game_type: str
    mechanics: list[str]
    user_interface: dict

class TestReport(BaseModel):
    bug_count: int
    bugs: list[str]
    suggestions: list[str]

class GameBuilderCrew:
    def game_designer(self):
        return Agent(
            role="Game Designer",
            goal="Design engaging game mechanics and user experience",
            backstory="Game design specialist with expertise in Python games",
            verbose=True
        )

    def python_developer(self):
        return Agent(
            role="Python Developer",
            goal="Implement game code in Python",
            backstory="Python developer specializing in game development",
            tools=[CodeExecutionTool()],
            verbose=True
        )

    def qa_tester(self):
        return Agent(
            role="QA Tester",
            goal="Test game functionality and report bugs",
            backstory="Quality assurance specialist for game testing",
            tools=[PythonREPL()],
            verbose=True
        )

    def design_task(self):
        return Task(
            description="Design game concept with mechanics and UI",
            expected_output="Game design document with detailed mechanics",
            output_pydantic=GameDesign,
            agent=self.game_designer()
        )

    def implementation_task(self):
        return Task(
            description="Implement Python game code based on design",
            expected_output="Working Python game code",
            agent=self.python_developer(),
            context=[self.design_task()]
        )

    def testing_task(self):
        return Task(
            description="Test game and provide feedback on bugs and improvements",
            expected_output="Bug report and improvement suggestions",
            output_pydantic=TestReport,
            agent=self.qa_tester(),
            context=[self.implementation_task()]
        )

    def crew(self):
        return Crew(
            agents=[self.game_designer(), self.python_developer(), self.qa_tester()],
            tasks=[self.design_task(), self.implementation_task(), self.testing_task()],
            verbose=True,
            process="sequential"
        )
