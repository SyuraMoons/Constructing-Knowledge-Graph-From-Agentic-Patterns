"""CrewAI pattern: write_book_flow"""
from crewai import Agent, Crew, Task
from crewai.flow import Flow, listen, start, parallel
from pydantic import BaseModel

class Chapter(BaseModel):
    chapter_id: int
    title: str
    content: str

class Book(BaseModel):
    title: str
    chapters: list[Chapter]
    final_content: str

class WriteBookFlow(Flow):
    @start()
    def create_outline(self):
        planner = Agent(
            role="Outline Planner",
            goal="Create comprehensive book outline with chapter structure",
            backstory="Experienced book structure consultant"
        )
        outline_task = Task(
            description="Create detailed book outline with 10 chapters",
            expected_output="Book outline with chapter titles and summaries",
            agent=planner
        )
        return outline_task.execute()

    @listen(create_outline)
    @parallel(degree=5)
    def write_chapter(self, outline, chapter_id):
        writer = Agent(
            role=f"Chapter Writer {chapter_id}",
            goal="Write engaging chapter content",
            backstory="Professional author with expertise in storytelling"
        )
        chapter_task = Task(
            description=f"Write Chapter {chapter_id} based on outline",
            expected_output="Complete chapter content",
            output_pydantic=Chapter,
            agent=writer
        )
        return chapter_task.execute()

    @listen(write_chapter)
    def aggregate_chapters(self, chapters):
        aggregator = Agent(
            role="Content Aggregator",
            goal="Combine chapters into cohesive book",
            backstory="Editorial coordinator specializing in book assembly"
        )
        aggregate_task = Task(
            description="Combine all chapters into single manuscript",
            expected_output="Aggregated book content",
            agent=aggregator
        )
        return aggregate_task.execute()

    @listen(aggregate_chapters)
    def edit_book(self, manuscript):
        editor = Agent(
            role="Senior Editor",
            goal="Review and harmonize all chapters",
            backstory="Award-winning book editor"
        )
        editing_task = Task(
            description="Edit complete manuscript for consistency and quality",
            expected_output="Final edited book",
            output_pydantic=Book,
            agent=editor
        )
        return editing_task.execute()
