"""CrewAI pattern: stock_analysis"""
from crewai import Agent, Crew, Task
from crewai_tools import SECTool, YahooFinanceTool, SerperDevTool
from pydantic import BaseModel

class InvestmentAdvice(BaseModel):
    recommendation: str
    rationale: str
    risk_level: str
    target_price: float

class StockAnalysisCrew:
    def __init__(self):
        self.sec_tool = SECTool()
        self.finance_tool = YahooFinanceTool()
        self.serper_tool = SerperDevTool()

    def data_analyst(self):
        return Agent(
            role="Financial Data Analyst",
            goal="Analyze SEC filings and financial statements",
            backstory="CFA charterholder specializing in financial statement analysis",
            tools=[self.sec_tool, self.finance_tool],
            verbose=True
        )

    def market_researcher(self):
        return Agent(
            role="Market Researcher",
            goal="Research market trends and competitive landscape",
            backstory="Market intelligence specialist with deep sector knowledge",
            tools=[self.serper_tool],
            verbose=True
        )

    def investment_advisor(self):
        return Agent(
            role="Investment Advisor",
            goal="Provide investment recommendations based on analysis",
            backstory="Senior investment advisor with 15+ years experience",
            verbose=True
        )

    def financial_analysis_task(self):
        return Task(
            description="Analyze financial statements and SEC filings",
            expected_output="Comprehensive financial metrics report",
            agent=self.data_analyst()
        )

    def market_research_task(self):
        return Task(
            description="Research market conditions and competitor analysis",
            expected_output="Market trends and competitive analysis report",
            agent=self.market_researcher()
        )

    def recommendation_task(self):
        return Task(
            description="Generate investment recommendation with rationale",
            expected_output="Buy/Hold/Sell recommendation with detailed rationale",
            output_pydantic=InvestmentAdvice,
            agent=self.investment_advisor(),
            context=[self.financial_analysis_task(), self.market_research_task()]
        )

    def crew(self):
        return Crew(
            agents=[self.data_analyst(), self.market_researcher(), self.investment_advisor()],
            tasks=[self.financial_analysis_task(), self.market_research_task(), self.recommendation_task()],
            verbose=True,
            process="sequential"
        )
