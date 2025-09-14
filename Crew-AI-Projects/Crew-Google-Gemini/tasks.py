from crewai import Task
from tools import tool
from agents import news_research_agent, write_code_agent


from agents import news_research_agent, write_code_agent

research_task = Task(
    description=(
        "Identify the next big trend in the topic {topic}"
        "Focus on identifying pros and cons"
    ),
    expected_output="Comprehensive 1 paragraph report on the latest advancements in AI technology.",
    agent=news_research_agent,
    tools=[tool]
)

write_task = Task(
    agent=write_code_agent,
    tools=[tool],
    description="Write a detailed article on the topic {topic} based on the research findings.",
    expected_output="A well-structured article with words upto 250",
    async_execution=False,
    output_file="output_article.txt"
)
