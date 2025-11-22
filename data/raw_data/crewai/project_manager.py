"""CrewAI pattern: job_posting"""
from crewai import Agent, Crew, Task
from crewai_tools import KeywordResearchTool
from pydantic import BaseModel

class JobPosting(BaseModel):
    title: str
    description: str
    requirements: list[str]
    keywords: list[str]
    salary_range: str

class JobPostingCrew:
    def hr_specialist(self):
        return Agent(
            role="HR Specialist",
            goal="Define job requirements and qualifications",
            backstory="HR professional with talent acquisition expertise",
            verbose=True
        )

    def copywriter(self):
        return Agent(
            role="Copywriter",
            goal="Write compelling job descriptions",
            backstory="Professional writer specializing in job postings",
            verbose=True
        )

    def seo_specialist(self):
        return Agent(
            role="SEO Specialist",
            goal="Optimize job posting for search visibility",
            backstory="SEO expert specializing in job board optimization",
            tools=[KeywordResearchTool()],
            verbose=True
        )

    def requirements_task(self):
        return Task(
            description="Define job requirements and qualifications",
            expected_output="Detailed requirements and qualifications list",
            agent=self.hr_specialist()
        )

    def description_task(self):
        return Task(
            description="Write engaging job description",
            expected_output="Complete job description with benefits",
            agent=self.copywriter(),
            context=[self.requirements_task()]
        )

    def optimization_task(self):
        return Task(
            description="Optimize posting for SEO with relevant keywords",
            expected_output="Optimized job posting with keywords",
            output_pydantic=JobPosting,
            agent=self.seo_specialist(),
            context=[self.description_task()]
        )

    def crew(self):
        return Crew(
            agents=[self.hr_specialist(), self.copywriter(), self.seo_specialist()],
            tasks=[self.requirements_task(), self.description_task(), self.optimization_task()],
            verbose=True,
            process="sequential"
        )
