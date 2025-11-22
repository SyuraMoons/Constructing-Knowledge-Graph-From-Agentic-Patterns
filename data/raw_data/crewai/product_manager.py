"""CrewAI pattern: landing_page_generator"""
from crewai import Agent, Crew, Task
from crewai_tools import HTMLGeneratorTool
from pydantic import BaseModel

class LandingPage(BaseModel):
    hero_section: str
    features: list[str]
    testimonials: list[str]
    cta_text: str
    html_code: str

class LandingPageCrew:
    def ux_researcher(self):
        return Agent(
            role="UX Researcher",
            goal="Analyze user needs and design optimal user experience",
            backstory="UX research specialist with conversion optimization expertise",
            verbose=True
        )

    def copywriter(self):
        return Agent(
            role="Copywriter",
            goal="Create compelling landing page copy",
            backstory="Conversion copywriter with proven track record",
            verbose=True
        )

    def web_designer(self):
        return Agent(
            role="Web Designer",
            goal="Design complete landing page layout",
            backstory="Web designer specializing in high-converting landing pages",
            tools=[HTMLGeneratorTool()],
            verbose=True
        )

    def research_task(self):
        return Task(
            description="Research target audience and identify pain points",
            expected_output="User persona and pain points analysis",
            agent=self.ux_researcher()
        )

    def copy_creation_task(self):
        return Task(
            description="Write landing page copy including hero, features, and CTAs",
            expected_output="Complete landing page copy",
            agent=self.copywriter(),
            context=[self.research_task()]
        )

    def design_task(self):
        return Task(
            description="Create complete landing page with HTML/CSS",
            expected_output="Complete HTML landing page",
            output_pydantic=LandingPage,
            agent=self.web_designer(),
            context=[self.copy_creation_task()]
        )

    def crew(self):
        return Crew(
            agents=[self.ux_researcher(), self.copywriter(), self.web_designer()],
            tasks=[self.research_task(), self.copy_creation_task(), self.design_task()],
            verbose=True,
            process="sequential"
        )
