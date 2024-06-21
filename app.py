import os
from dotenv import load_dotenv
import gradio as gr
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage, Settings,
)
from llama_index.llms.ollama import Ollama

# Load environment variables
load_dotenv()

# Path to your local corpus directory
PERSIST_DIR = './storage2'
corpus_directory = 'articles'

# Configure the settings
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

# Initialize or load the index
if not os.path.exists(PERSIST_DIR):
    # Load the documents and create the index
    documents = SimpleDirectoryReader(corpus_directory).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # Store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # Load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

def chatbot_response(user_input):
    response = query_engine.query(user_input)
    return str(response)

# Create a Gradio interface
interface = gr.Interface(fn=chatbot_response, inputs="text", outputs="text", title="Chatbot")

# Launch the interface
if __name__ == "__main__":
    interface.launch()
