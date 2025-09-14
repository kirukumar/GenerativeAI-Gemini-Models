from crewai import Crew, Process
from tasks import research_task, writer_task
from agents import blog_researcher, blog_writer

blog_creator_crew = Crew(
    agents=[blog_researcher, blog_writer],
    tasks=[research_task, writer_task],
    process = Process.SEQUENTIAL,
    memory=True,
    cache=True,
    max_rpm=300,
    share_crew=True
)


## Start the task execution
if __name__ == "__main__":
    result = blog_creator_crew.kickoff(inputs={"topic": "AI VS ML VS DL vs Data Science"})
    print(result)