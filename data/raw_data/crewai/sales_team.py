"""CrewAI pattern: lead_score_flow"""
from crewai import Agent, Crew, Task
from crewai.flow import Flow, listen, start
from crewai_tools import CRMTool
from pydantic import BaseModel

class LeadScore(BaseModel):
    lead_id: str
    score: int
    criteria: dict
    recommendation: str

class LeadScoreFlow(Flow):
    @start()
    def analyze_lead(self, lead_data):
        analyzer = Agent(
            role="Lead Analyzer",
            goal="Analyze lead data and extract insights",
            backstory="Expert at evaluating lead quality",
            tools=[CRMTool()]
        )
        analysis_task = Task(
            description=f"Analyze lead data: {lead_data}",
            expected_output="Lead analysis report",
            agent=analyzer
        )
        return analysis_task.execute()

    @listen(analyze_lead)
    def calculate_score(self, analysis):
        scoring_agent = Agent(
            role="Scoring Agent",
            goal="Assign qualification scores to leads",
            backstory="Data-driven lead scoring specialist"
        )
        scoring_task = Task(
            description="Calculate lead score based on analysis",
            expected_output="Lead score (0-100)",
            output_pydantic=LeadScore,
            agent=scoring_agent
        )
        score_result = scoring_task.execute()
        return score_result

    @listen(calculate_score)
    def route_lead(self, score_result):
        if score_result.score > 80:
            return self.high_value_review(score_result)
        elif score_result.score > 50:
            return self.route_to_sales_team_a(score_result)
        else:
            return self.route_to_nurture_team(score_result)

    def high_value_review(self, score_result):
        reviewer = Agent(
            role="Sales Manager",
            goal="Review high-value leads",
            backstory="Senior sales manager with deal closure expertise",
            human_input=True
        )
        review_task = Task(
            description=f"Review high-value lead with score {score_result.score}",
            expected_output="Approval decision",
            agent=reviewer
        )
        return review_task.execute()

    def route_to_sales_team_a(self, score_result):
        router = Agent(
            role="Lead Router",
            goal="Route qualified leads to appropriate sales teams",
            backstory="Lead distribution specialist"
        )
        routing_task = Task(
            description="Route medium-value lead to Sales Team A",
            expected_output="Routing confirmation",
            agent=router
        )
        return routing_task.execute()

    def route_to_nurture_team(self, score_result):
        router = Agent(
            role="Lead Router",
            goal="Route leads to nurture campaigns",
            backstory="Marketing automation specialist"
        )
        nurture_task = Task(
            description="Add low-score lead to nurture campaign",
            expected_output="Nurture campaign enrollment confirmation",
            agent=router
        )
        return nurture_task.execute()
