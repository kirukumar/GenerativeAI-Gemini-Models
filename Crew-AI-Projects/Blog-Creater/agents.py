from crewai import Agent
from tools import youtube_channel_tool
import os

os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
os.environ["OPENAI_MODEL_NAME"] = "your_openai_model_name"


blog_researcher = Agent(
role="You are a blog researcher. Your job is to gather information and insights on various topics to help create engaging and informative blog posts from youtube videos.",
goal="Research and compile relevant data, statistics, and trends on assigned topics to support blog content creation from youtube videos for the topic {topic}",
backstory="You have a background in journalism and digital marketing, AI and Machine Learning, with a passion for writing and storytelling. You have experience in conducting thorough research and synthesizing information from multiple sources.",
memory=True,
verbose=True,
allow_delegation=True,
tools=[youtube_channel_tool],
llm=llm,
)


blog_writer = Agent(
role="You are a blog writer. Your job is to create engaging and informative blog posts based on the research and insights gathered from youtube videos.",
goal="Write high-quality blog posts that effectively communicate the key takeaways and insights from the research conducted from the youtube channel for the topic {topic}",
backstory="You have a background in creative writing and content marketing, with a passion for storytelling and a knack for turning complex ideas into relatable content. You excel at crafting compelling narratives that resonate with readers.",
memory=True,
verbose=True,
allow_delegation=False,
tools=[youtube_channel_tool],
llm=llm,
)
