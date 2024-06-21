import os
import gradio as gr
import torch
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage, Settings,
)
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

load_dotenv()

# Path to your local corpus directory
PERSIST_DIR = './storage'
corpus_directory = 'articles'

# Configure the settings
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# Load the Llama 3 model and tokenizer
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(model_id, use_auth_token=True, torch_dtype=torch.float16)


# Initialize the Llama 3 pipeline
llama3_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
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


def chatbot_response(user_input):
    # Retrieve context from the vector store
    context = query_engine.query(user_input)
    context_str = str(context)

    # Combine user input with retrieved context
    combined_input = f"{context_str}\n\nUser: {user_input}\nAssistant:"

    # Generate a response using the Llama 3 pipeline
    outputs = llama3_pipeline(
        combined_input,
        max_new_tokens=256,
        eos_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    assistant_response = outputs[0]["generated_text"].split("Assistant:")[1].strip()
    return assistant_response

interface = gr.Interface(fn=chatbot_response, inputs="text", outputs="text", title="Testing HF deployment")


# Launch the interface
if __name__ == "__main__":
    interface.launch()
