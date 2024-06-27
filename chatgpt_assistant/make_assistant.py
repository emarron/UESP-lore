from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

# this is your project key
key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=key)

description = "Elder Scrolls Lore Bot"
instructions = """You are a librarian of a library throughout Elder Scrolls history. Your role is to help readers 
summarize, connect topics, and find books in your library. If you cannot find something relevant, kindly respond 
with, "I'm sorry, I don't have enough context."""

# I recommend chatgpt 3.5 turbo because it is fast and cheap.
assistant = client.beta.assistants.create(
    name="Elder Scrolls Lore Bot",
    description=description,
    instructions=instructions,
    model="gpt-3.5-turbo",
    tools=[{"type": "file_search"}],
)


# this will give you the assistant ID to add to your .env
print(assistant)