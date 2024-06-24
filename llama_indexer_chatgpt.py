import json
import os.path
import gr as gr
import gradio as gr
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage, Document,
)
from chat_bot_resources.config import DATA_DIRECTORY

from chat_bot_resources.resources import create_or_load_index

PERSIST_DIR = 'storage_chatgpt'
articles_directory = DATA_DIRECTORY


load_dotenv()
index = create_or_load_index(PERSIST_DIR, article_directory)
query_engine = index.as_query_engine()


def chatbot_response(message, history):
    response = query_engine.query(message)
    return str(response)


iface = gr.ChatInterface(
    fn=chatbot_response,
    title="UESP Lore Chatbot",
    description="Ask questions about The Elder Scrolls lore!",
    # examples=["Who is Vivec?", "Tell me about the Oblivion Crisis", "Who is King Edward?"],
    # cache_examples=False,
)

# Launch the interface
if __name__ == "__main__":
    # chat()
    iface.launch()
