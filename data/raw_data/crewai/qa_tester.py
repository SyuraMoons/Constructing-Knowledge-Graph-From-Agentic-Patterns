"""CrewAI pattern: crewai_langgraph"""
from crewai import Agent, Crew, Task
from langgraph.graph import StateGraph
from pydantic import BaseModel

class WorkflowState(BaseModel):
    current_crew: str = ""
    crew_outputs: list[dict] = []
    final_result: str = ""

class CrewAILangGraphIntegration:
    def build_research_crew(self):
        researcher = Agent(
            role="Researcher",
            goal="Conduct thorough research on topics",
            backstory="Research specialist with academic background"
        )
        analyst = Agent(
            role="Analyst",
            goal="Analyze research findings",
            backstory="Data analyst with critical thinking skills"
        )
        research_task = Task(
            description="Research the given topic",
            expected_output="Research report",
            agent=researcher
        )
        analysis_task = Task(
            description="Analyze research findings",
            expected_output="Analysis report",
            agent=analyst,
            context=[research_task]
        )
        return Crew(
            agents=[researcher, analyst],
            tasks=[research_task, analysis_task]
        )

    def build_analysis_crew(self):
        data_analyst = Agent(
            role="Data Analyst",
            goal="Perform data analysis",
            backstory="Statistical analyst with ML background"
        )
        strategist = Agent(
            role="Strategist",
            goal="Develop strategic recommendations",
            backstory="Business strategist with industry experience"
        )
        data_task = Task(
            description="Analyze data patterns",
            expected_output="Data analysis report",
            agent=data_analyst
        )
        strategy_task = Task(
            description="Develop strategic recommendations",
            expected_output="Strategy document",
            agent=strategist,
            context=[data_task]
        )
        return Crew(
            agents=[data_analyst, strategist],
            tasks=[data_task, strategy_task]
        )

    def execute_crew_node(self, state, crew):
        result = crew.kickoff()
        state["crew_outputs"].append(result)
        return state

    def build_workflow(self):
        workflow = StateGraph(WorkflowState)
        
        # Add crew execution nodes
        workflow.add_node("research_crew", lambda state: self.execute_crew_node(state, self.build_research_crew()))
        workflow.add_node("analysis_crew", lambda state: self.execute_crew_node(state, self.build_analysis_crew()))
        workflow.add_node("output_node", lambda state: state)
        
        # Define edges
        workflow.add_edge("research_crew", "analysis_crew")
        workflow.add_edge("analysis_crew", "output_node")
        
        # Set entry and finish points
        workflow.set_entry_point("research_crew")
        workflow.set_finish_point("output_node")
        
        return workflow.compile()
