"""CrewAI pattern: recruitment"""
from crewai import Agent, Crew, Task
from crewai_tools import LinkedInScraperTool, JobBoardAPI, CVParserTool, CalendarTool
from pydantic import BaseModel

class CandidateRanking(BaseModel):
    candidates: list[dict]
    scores: list[int]
    match_percentages: list[float]
    rationale: str

class RecruitmentCrew:
    def __init__(self):
        self.linkedin_tool = LinkedInScraperTool()
        self.job_board_tool = JobBoardAPI()
        self.cv_parser = CVParserTool()
        self.calendar_tool = CalendarTool()

    def sourcing_specialist(self):
        return Agent(
            role="Sourcing Specialist",
            goal="Find qualified candidates from multiple sources",
            backstory="Talent sourcing expert with extensive recruiting network",
            tools=[self.linkedin_tool, self.job_board_tool],
            verbose=True
        )

    def resume_analyzer(self):
        return Agent(
            role="Resume Analyzer",
            goal="Screen and rank candidates based on qualifications",
            backstory="HR specialist with expertise in candidate evaluation",
            tools=[self.cv_parser],
            verbose=True
        )

    def interview_coordinator(self):
        return Agent(
            role="Interview Coordinator",
            goal="Schedule interviews with qualified candidates",
            backstory="Recruitment coordinator specializing in interview logistics",
            tools=[self.calendar_tool],
            verbose=True
        )

    def sourcing_task(self):
        return Task(
            description="Source candidates for open position",
            expected_output="List of 20+ qualified candidates with profiles",
            agent=self.sourcing_specialist()
        )

    def screening_task(self):
        return Task(
            description="Analyze and rank candidates by qualification scores",
            expected_output="Ranked candidate list with scores and match percentages",
            output_pydantic=CandidateRanking,
            agent=self.resume_analyzer(),
            context=[self.sourcing_task()]
        )

    def scheduling_task(self):
        return Task(
            description="Schedule interviews with top candidates",
            expected_output="Interview calendar with confirmed time slots",
            agent=self.interview_coordinator(),
            context=[self.screening_task()]
        )

    def crew(self):
        return Crew(
            agents=[self.sourcing_specialist(), self.resume_analyzer(), self.interview_coordinator()],
            tasks=[self.sourcing_task(), self.screening_task(), self.scheduling_task()],
            verbose=True,
            process="sequential"
        )
