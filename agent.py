from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner , OpenAIChatCompletionsModel, set_tracing_disabled
import os


load_dotenv()
set_tracing_disabled(True)

provide =AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

model = OpenAIChatCompletionsModel( 
    model= "gemini-2.0-flash-exp",
    openai_client= provide ,
)


# web developer

web_dev = Agent(
    name= "Web Developer Expert",
    instructions= "build responsive and performant web applications using the latest technologies and best practices",
    model= model,
    handoff_description="handoff to web developer if the task is related to web development",

)

# Mobile App Developer

Mobile_dev = Agent(
    name= "Mobile App developer Expert",
    instructions= "build mobile applications using modern frameworks",
    model= model,
    handoff_description="handoff to mobile app developer if the task is related to mobile app development",

)

# Marketing Agent

Marketing_agent = Agent(
    name= "Marketing  Expert Agent ",
    instructions= "create marketing strategies and content for the product",
    model= model,
    handoff_description="handoff to marketing agent if the task is related to marketing",
)


async def myAgent(user_input):
   manager = Agent(
      name = "Manager",
      instructions= "You will chat with the user and delegate tasks to specialized agents based on the their request",
      model= model,
      handoffs= [web_dev, Mobile_dev, Marketing_agent],
   )

   response = await Runner.run(
      manager,
      input= user_input
   )

   return response.final_output