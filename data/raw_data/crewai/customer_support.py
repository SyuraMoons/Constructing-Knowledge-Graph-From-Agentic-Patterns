"""CrewAI pattern: email_auto_responder_flow"""
from crewai import Agent, Crew, Task
from crewai.flow import Flow, listen, start
from pydantic import BaseModel

class EmailState(BaseModel):
    email_content: str = ""
    classification: str = ""
    response_draft: str = ""
    approved: bool = False

class EmailAutoResponderFlow(Flow[EmailState]):
    @start()
    def monitor_inbox(self):
        monitor_task = Task(
            description="Monitor inbox for new emails",
            expected_output="List of unread emails",
            agent=self.email_monitor_agent()
        )
        return monitor_task

    @listen(monitor_inbox)
    def classify_email(self, emails):
        classifier = self.email_classifier_agent()
        classification_task = Task(
            description="Classify email by priority and type",
            expected_output="Email classification (urgent/routine/spam)",
            agent=classifier
        )
        result = classification_task.execute()
        self.state.classification = result
        return result

    @listen(classify_email)
    def generate_response(self, classification):
        response_generator = self.response_generator_agent()
        response_task = Task(
            description="Generate appropriate email response",
            expected_output="Draft email response",
            agent=response_generator
        )
        result = response_task.execute()
        self.state.response_draft = result
        return result

    @listen(generate_response)
    def human_review(self, draft):
        reviewer = self.human_reviewer_agent()
        review_task = Task(
            description="Review and approve email response",
            expected_output="Approved/rejected with feedback",
            agent=reviewer,
            human_input=True
        )
        result = review_task.execute()
        self.state.approved = result.approved
        return result

    def email_monitor_agent(self):
        return Agent(
            role="Email Monitor",
            goal="Continuously monitor inbox for new emails",
            backstory="Automated email monitoring system"
        )

    def email_classifier_agent(self):
        return Agent(
            role="Email Classifier",
            goal="Categorize incoming emails by priority and type",
            backstory="AI email classification specialist"
        )

    def response_generator_agent(self):
        return Agent(
            role="Response Generator",
            goal="Generate appropriate email responses",
            backstory="Professional email response writer"
        )

    def human_reviewer_agent(self):
        return Agent(
            role="Human Reviewer",
            goal="Review and approve responses before sending",
            backstory="Email quality assurance manager",
            human_input=True
        )
