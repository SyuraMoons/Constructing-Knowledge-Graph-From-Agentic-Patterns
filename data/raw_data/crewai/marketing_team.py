"""CrewAI pattern: marketing_strategy"""
from crewai import Agent, Crew, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel

class MarketStrategy(BaseModel):
    name: str
    tactics: list
    channels: list
    kpis: list

class CampaignIdea(BaseModel):
    name: str
    description: str
    audience: str
    channel: str

class Copy(BaseModel):
    title: str
    body: str

class MarketingPostsCrew:
    def __init__(self):
        self.serper_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()

    def lead_market_analyst(self):
        return Agent(
            role="Lead Market Analyst",
            goal="Conduct amazing analysis of the products and competitors",
            backstory="You specialize in dissecting online business landscapes",
            tools=[self.serper_tool, self.scrape_tool],
            verbose=True
        )

    def chief_marketing_strategist(self):
        return Agent(
            role="Chief Marketing Strategist",
            goal="Synthesize amazing insights from product analysis",
            backstory="You are known for crafting bespoke marketing strategies",
            tools=[self.serper_tool, self.scrape_tool],
            verbose=True
        )

    def creative_content_creator(self):
        return Agent(
            role="Creative Content Creator",
            goal="Develop compelling and innovative content for campaigns",
            backstory="You excel in crafting narratives that resonate with audiences",
            verbose=True
        )

    def chief_creative_director(self):
        return Agent(
            role="Chief Creative Director",
            goal="Oversee the work done by your team",
            backstory="You ensure your team crafts the best possible content",
            verbose=True
        )

    def research_task(self):
        return Task(
            description="Conduct thorough research about {customer_domain}",
            expected_output="Complete report on customer and competitors",
            agent=self.lead_market_analyst()
        )

    def project_understanding_task(self):
        return Task(
            description="Understand the project details for {project_description}",
            expected_output="Detailed summary of the project",
            agent=self.chief_marketing_strategist()
        )

    def marketing_strategy_task(self):
        return Task(
            description="Formulate marketing strategy for {project_description}",
            expected_output="Marketing strategy with goals, tactics, channels, KPIs",
            output_pydantic=MarketStrategy,
            agent=self.chief_marketing_strategist()
        )

    def campaign_idea_task(self):
        return Task(
            description="Develop creative campaign ideas for {project_description}",
            expected_output="List of 5 campaign ideas",
            output_pydantic=CampaignIdea,
            agent=self.creative_content_creator()
        )

    def copy_creation_task(self):
        return Task(
            description="Create marketing copies based on approved campaigns",
            expected_output="Marketing copies for each campaign idea",
            output_pydantic=Copy,
            context=[self.campaign_idea_task()],
            agent=self.creative_content_creator()
        )

    def crew(self):
        return Crew(
            agents=[
                self.lead_market_analyst(),
                self.chief_marketing_strategist(),
                self.creative_content_creator()
            ],
            tasks=[
                self.research_task(),
                self.project_understanding_task(),
                self.marketing_strategy_task(),
                self.campaign_idea_task(),
                self.copy_creation_task()
            ],
            verbose=True,
            memory=False,
            process="sequential"
        )
