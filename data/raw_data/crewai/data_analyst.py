"""CrewAI pattern: match_profile_to_positions"""
from crewai import Agent, Crew, Task
from crewai_tools import CVParserTool, EmbeddingTool, VectorSearchTool
from pydantic import BaseModel

class CandidateProfile(BaseModel):
    skills: list[str]
    experience: str
    embedding: list[float]

class JobRecommendation(BaseModel):
    job_title: str
    company: str
    similarity_score: float
    match_reason: str

class MatchingCrew:
    def __init__(self):
        self.cv_parser = CVParserTool()
        self.embedding_tool = EmbeddingTool()
        self.vector_search = VectorSearchTool()

    def profile_analyzer(self):
        return Agent(
            role="Profile Analyzer",
            goal="Extract skills and experience from CV and generate embeddings",
            backstory="AI specialist in resume parsing and vector representation",
            tools=[self.cv_parser, self.embedding_tool],
            verbose=True
        )

    def job_matcher(self):
        return Agent(
            role="Job Matcher",
            goal="Find best matching positions using vector similarity",
            backstory="Matching algorithm specialist with ML expertise",
            tools=[self.vector_search],
            verbose=True
        )

    def recommendation_generator(self):
        return Agent(
            role="Recommendation Generator",
            goal="Generate personalized job recommendations with explanations",
            backstory="Career advisor with data science background",
            verbose=True
        )

    def profile_analysis_task(self):
        return Task(
            description="Analyze candidate profile and create embeddings",
            expected_output="Structured profile with vector embeddings",
            output_pydantic=CandidateProfile,
            agent=self.profile_analyzer()
        )

    def matching_task(self):
        return Task(
            description="Find matching positions using similarity search",
            expected_output="Ranked list of positions with similarity scores",
            agent=self.job_matcher(),
            context=[self.profile_analysis_task()]
        )

    def recommendation_task(self):
        return Task(
            description="Generate job recommendations with detailed explanations",
            expected_output="Personalized job recommendations with match reasons",
            output_pydantic=JobRecommendation,
            agent=self.recommendation_generator(),
            context=[self.matching_task()]
        )

    def crew(self):
        return Crew(
            agents=[self.profile_analyzer(), self.job_matcher(), self.recommendation_generator()],
            tasks=[self.profile_analysis_task(), self.matching_task(), self.recommendation_task()],
            verbose=True,
            process="sequential"
        )
