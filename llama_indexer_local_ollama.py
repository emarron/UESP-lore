import os
import json
import gradio as gr
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage, Settings, Document
)
from llama_index.llms.ollama import Ollama
from chat_bot_resources.config import DATA_DIRECTORY

from chat_bot_resources.resources import create_or_load_index

PERSIST_DIR = 'storage_local_ollama'
articles_directory = DATA_DIRECTORY

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

index = create_or_load_index(PERSIST_DIR, article_directory)
query_engine = index.as_query_engine()


def chatbot_response(message, history):
    response = query_engine.query(message)
    return str(response)


iface = gr.ChatInterface(
    fn=chatbot_response,
    title="UESP Lore Chatbot",
    description="Ask questions about The Elder Scrolls lore!",
)

# Launch the interface
if __name__ == "__main__":
    iface.launch()
