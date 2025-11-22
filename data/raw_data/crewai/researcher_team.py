"""CrewAI pattern: instagram_post"""
from crewai import Agent, Crew, Task
from crewai_tools import TrendAnalysisTool, ImageGenerationTool
from pydantic import BaseModel

class InstagramPost(BaseModel):
    caption: str
    hashtags: list[str]
    image_url: str

class InstagramCrew:
    def __init__(self):
        self.trend_tool = TrendAnalysisTool()
        self.image_tool = ImageGenerationTool()

    def content_strategist(self):
        return Agent(
            role="Content Strategist",
            goal="Plan engaging Instagram content",
            backstory="Social media strategist with expertise in Instagram growth",
            tools=[self.trend_tool],
            verbose=True
        )

    def creative_designer(self):
        return Agent(
            role="Creative Designer",
            goal="Design visually appealing Instagram posts",
            backstory="Visual designer specializing in social media content",
            tools=[self.image_tool],
            verbose=True
        )

    def content_planning_task(self):
        return Task(
            description="Create 30-day Instagram content calendar",
            expected_output="Content calendar with post ideas and themes",
            agent=self.content_strategist()
        )

    def post_creation_task(self):
        return Task(
            description="Generate Instagram post with caption and image",
            expected_output="Complete Instagram post with caption, hashtags, and image",
            output_pydantic=InstagramPost,
            agent=self.creative_designer(),
            context=[self.content_planning_task()]
        )

    def crew(self):
        return Crew(
            agents=[self.content_strategist(), self.creative_designer()],
            tasks=[self.content_planning_task(), self.post_creation_task()],
            verbose=True,
            process="sequential"
        )
