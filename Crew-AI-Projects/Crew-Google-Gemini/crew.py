from crewai import Crew, Process
from agents import news_research_agent, write_code_agent
from tasks import research_task, write_task

crew = Crew(
    
    agents=[
        news_research_agent,
        write_code_agent
    ],
    process=Process.sequential,
        tasks=[
            research_task,
            write_task
        ]
)

result = crew.kickoff(inputs={"topic": "Artificial Intelligence"})
print("Final Output:", result)