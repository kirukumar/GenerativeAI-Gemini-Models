from crewai import Agent, LLM


from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from tools import tool
import os
load_dotenv()

llm = LLM(
model="gemini/gemini-2.5-pro",
temperature=0.7,
api_key=os.getenv("GOOGLE_API_KEY")
)


news_research_agent = Agent(
llm=llm,
role="Research Assistant",
goal="Uncover ground breaking technologies in the topic {topic}",
verbose=True,
memory=True,
allow_delegation=True,
backstory="You're a research assistant that helps to find the latest advancements in various fields of technology. You have access to a wide range of resources and can analyze information quickly and accurately.",
tools=[tool],
);

write_code_agent = Agent(
tools=[tool],
llm=llm,
role="Writer",
goal="Write a well-structured and detailed article on the topic {topic}",
verbose=True,
memory=True,
allow_delegation=False,
backstory="You're a writer that specializes in creating high-quality content on various topics. You have access to a wealth of information and can craft articles that are both informative and engaging.",
);
