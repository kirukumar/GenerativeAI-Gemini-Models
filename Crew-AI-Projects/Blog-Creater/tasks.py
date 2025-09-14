from crewai import Task
from tools import youtube_channel_tool
from agents import blog_researcher, blog_writer

## Research Task

research_task = Task(
    name="Blog Research Task",
    description=(
        "Identify the video {topic} from the youtube channel"
        "Research and gather information from YouTube videos to support blog content creation."
    ),
    expected_output=(
        "A comprehensive research report of 3 paragraphs including key data, statistics, and trends"
        "relevant to the assigned topic from youtube videos."
    ),
    agent=blog_researcher,
    tools=[youtube_channel_tool],
)

writer_task = Task(
    name="Blog Writing Task",
    description=(
        "Create an engaging and informative blog post based on the research"
        "and insights gathered from YouTube videos."
    ),
    expected_output=(
        "Summarize the info from the youtube channel for the topic {topic} and create a well-structured blog post of 500-700 words"
    ),
    agent=blog_writer,
    async_execution=True,
    tools=[youtube_channel_tool],
    output_to_file="blog_post.txt",
)