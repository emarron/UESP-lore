import os
import gradio as gr
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage, Settings,
)
from llama_index.llms.huggingface import HuggingFaceLLM
from transformers import BitsAndBytesConfig

load_dotenv()

# Path to your local corpus directory
PERSIST_DIR = './storage_local_tinyllama'
corpus_directory = 'articles'

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    # bnb_4bit_compute_dtype=torch.float16,
    # bnb_4bit_quant_type="nf4",
    # bnb_4bit_use_double_quant=True,
)

# Configure the settings
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

Settings.llm = HuggingFaceLLM(
    model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    tokenizer_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    context_window=2048,
    max_new_tokens=256,
    model_kwargs={"quantization_config": quantization_config},
    generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
    device_map="cuda", # try to force this to cuda.
)

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


# def chat():
#     print("Chatbot is ready. Type 'exit' to end the conversation.")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == 'exit':
#             print("Ending the chat. Goodbye!")
#             break
#         response = query_engine.query(user_input)
#         print(f"Chatbot: {response}")

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
