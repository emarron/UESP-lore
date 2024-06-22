import os.path
import gradio as gr
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage, Settings,
)
from llama_index.llms.ollama import Ollama

# Path to your local corpus directory
PERSIST_DIR = 'storage_local_ollama'
corpus_directory = 'articles'

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

Settings.llm = Ollama(model="llama3", request_timeout=360.0)

load_dotenv()
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader(corpus_directory).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

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