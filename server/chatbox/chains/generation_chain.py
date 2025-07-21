from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from server.chatbox.prompts.generation_prompt import generation_prompt
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7,
)

generation_chain: Runnable = generation_prompt | llm
