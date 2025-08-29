import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# now trying with google gemini api key
from langchain_google_genai import ChatGoogleGenerativeAI

from crewai import LLM


from dotenv import load_dotenv

load_dotenv()

# --- IMPORTANT ---
# Set up your API keys as environment variables
# You can get a free Serper API key at https://serper.dev/
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
# os.environ["SERPER_API_KEY"] = "YOUR_SERPER_API_KEY"


google_api_key = os.getenv("GEMINI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

print(google_api_key)
print(serper_api_key)
# Set the Serper API key for the tool to use
os.environ["SERPER_API_KEY"] = serper_api_key


# --- 1. Define Tools ---
# Initialize the search tool
search_tool = SerperDevTool()



# --- 3. Instantiate the Gemini LLM with the API Key ---
# This is the corrected instantiation, passing the key directly.
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=google_api_key,
#     # api_key=google_api_key,
#     verbose=True,
#     temperature=0.7,
# )


"""
Cant't use langchain class here due to litellm problem 
for litellm use crewai LLM class and set the api var name to ```GEMINI_API_KEY```
"""

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)

# --- 2. Define Your Agents ---
# Define the Researcher Agent
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover the latest news and developments on a given topic.',
  backstory="""You are a seasoned research analyst, known for your ability to dig up insightful and relevant information from the web.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool],
  llm=llm
)

# Define the Writer Agent
writer = Agent(
  role='Content Strategist',
  goal='Craft compelling and summarized content from research findings.',
  backstory="""You are a renowned Content Strategist, known for your ability to transform complex information into clear and engaging summaries.""",
  verbose=True,
  allow_delegation=False , # Set to False for this simple project
  llm=llm
)

# --- 3. Create Tasks for Your Agents ---
# Create the research task
research_task = Task(
  description="""Conduct a comprehensive analysis of the latest news on {topic}.
  Identify key trends, major events, and important figures.""",
  expected_output='A full analysis report with key findings.',
  agent=researcher
)

# Create the writing task
write_task = Task(
  description="""Compose a concise and engaging summary of the research findings on {topic}.
  Focus on the most critical information and present it in a clear, easy-to-read format.""",
  expected_output='A 3-paragraph summary of the key news and developments.',
  agent=writer
)

# --- 4. Assemble and Run Your Crew ---
# Create the Crew with a sequential process
# news_crew = Crew(
#   agents=[researcher, writer],
#   tasks=[research_task, write_task],
#   process=Process.sequential
# )




# --- Assemble the Crew WITH THE GEMINI LLM ---
news_crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential
  # llm=llm  # <-- Pass the Gemini model to the crew
)

# Start the Crew's work
# The topic is passed as a dictionary input to the kickoff method
print("######################")
print("Starting the crew's work on the topic: AI in healthcare")
print("######################")

result = news_crew.kickoff(inputs={'topic': 'AI in healthcare'})

print("\n\n######################")
print("Crew's work completed!")
print("######################\n")
print("Final Result:")
print(result)




# pip install crewai duckduckgo-search
# pip install 'crewai[tools]'


























# import os
# from crewai import Agent
# from crewai_tools import SerperDevTool

# from dotenv import load_dotenv

# load_dotenv()



# search_tool = SerperDevTool()

# # Define the Researcher Agent
# researcher = Agent(
#   role='Senior Research Analyst',
#   goal='Uncover the latest news and developments on a given topic.',
#   backstory="""You are a seasoned research analyst, known for your ability to dig up insightful and relevant information from the web.""",
#   verbose=True,
#   allow_delegation=False,
#   tools=[search_tool]
# )

# # Define the Writer Agent
# writer = Agent(
#   role='Content Strategist',
#   goal='Craft compelling and summarized content from research findings.',
#   backstory="""You are a renowned Content Strategist, known for your ability to transform complex information into clear and engaging summaries.""",
#   verbose=True,
#   allow_delegation=True
# )


# from crewai import Task

# # Create the research task
# research_task = Task(
#   description="""Conduct a comprehensive analysis of the latest news on {topic}.
#   Identify key trends, major events, and important figures.""",
#   expected_output='A full analysis report with key findings.',
#   agent=researcher
# )

# # Create the writing task
# write_task = Task(
#   description="""Compose a concise and engaging summary of the research findings on {topic}.
#   Focus on the most critical information and present it in a clear, easy-to-read format.""",
#   expected_output='A 3-paragraph summary of the key news and developments.',
#   agent=writer
# )


# from crewai import Crew, Process

# # Create the Crew
# news_crew = Crew(
#   agents=[researcher, writer],
#   tasks=[research_task, write_task],
#   process=Process.sequential
# )

# # Start the Crew's work
# result = news_crew.kickoff(inputs={'topic': 'AI in healthcare'})

# print("######################")
# print(result)