"""CrewAI pattern: content_creator_flow"""
from crewai import Agent, Crew, Task
from crewai.flow import Flow, listen, start
from pydantic import BaseModel

class ContentCreatorState(BaseModel):
    current_topic: str = ""
    blog_content: str = ""
    linkedin_content: str = ""
    research_content: str = ""

class ContentCreatorFlow(Flow[ContentCreatorState]):
    @start()
    def generate_blog_content(self):
        blog_crew = self.build_blog_crew()
        result = blog_crew.kickoff()
        self.state.blog_content = result
        return result

    @listen(generate_blog_content)
    def generate_linkedin_content(self, blog_result):
        linkedin_crew = self.build_linkedin_crew()
        result = linkedin_crew.kickoff()
        self.state.linkedin_content = result
        return result

    @listen(generate_blog_content)
    def generate_research_content(self, blog_result):
        research_crew = self.build_research_crew()
        result = research_crew.kickoff()
        self.state.research_content = result
        return result

    def build_blog_crew(self):
        blog_researcher = Agent(
            role="Blog Researcher",
            goal="Research trending topics for blog posts",
            backstory="Expert at identifying viral blog topics"
        )
        blog_writer = Agent(
            role="Blog Writer",
            goal="Write engaging blog posts",
            backstory="Professional content writer"
        )
        research_task = Task(
            description="Research blog topic: {topic}",
            expected_output="Blog research report",
            agent=blog_researcher
        )
        writing_task = Task(
            description="Write blog post based on research",
            expected_output="Complete blog post",
            agent=blog_writer,
            context=[research_task]
        )
        return Crew(agents=[blog_researcher, blog_writer],
                   tasks=[research_task, writing_task])

    def build_linkedin_crew(self):
        linkedin_strategist = Agent(
            role="LinkedIn Strategist",
            goal="Create LinkedIn content strategy",
            backstory="LinkedIn marketing expert"
        )
        linkedin_creator = Agent(
            role="LinkedIn Content Creator",
            goal="Write engaging LinkedIn posts",
            backstory="Social media content specialist"
        )
        strategy_task = Task(
            description="Develop LinkedIn strategy",
            expected_output="LinkedIn content strategy",
            agent=linkedin_strategist
        )
        creation_task = Task(
            description="Create LinkedIn post",
            expected_output="LinkedIn post with hashtags",
            agent=linkedin_creator,
            context=[strategy_task]
        )
        return Crew(agents=[linkedin_strategist, linkedin_creator],
                   tasks=[strategy_task, creation_task])

    def build_research_crew(self):
        research_analyst = Agent(
            role="Research Analyst",
            goal="Conduct deep research analysis",
            backstory="Academic researcher with industry experience"
        )
        report_writer = Agent(
            role="Report Writer",
            goal="Write comprehensive research reports",
            backstory="Technical writer specializing in reports"
        )
        analysis_task = Task(
            description="Analyze research data",
            expected_output="Research analysis",
            agent=research_analyst
        )
        report_task = Task(
            description="Write research report",
            expected_output="Complete research report",
            agent=report_writer,
            context=[analysis_task]
        )
        return Crew(agents=[research_analyst, report_writer],
                   tasks=[analysis_task, report_task])
