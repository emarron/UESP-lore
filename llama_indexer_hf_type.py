import json
import gradio as gr
from dotenv import load_dotenv
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.huggingface import HuggingFaceLLM
from chat_bot_resources.config import DATA_DIRECTORY

from chat_bot_resources.resources import create_or_load_index, messages_to_prompt_phi, completion_to_prompt_phi, \
    messages_to_prompt_llama3, completion_to_prompt_llama3
from llama_index.embeddings.openai import OpenAIEmbedding

load_dotenv()

# Load model configurations from JSON file
with open('model_configs/hf_model_configs.json', 'r') as f:
    MODEL_CONFIG = json.load(f)

# List available models
model_names = list(MODEL_CONFIG.keys())
print("Available models:")
for idx, name in enumerate(model_names):
    print(f"[{idx}] {name}")

# Prompt user to select a model
while True:
    try:
        model_choice_idx = int(input("Enter the number of the model you want to use: "))
        if 0 <= model_choice_idx < len(model_names):
            MODEL_CHOICE = model_names[model_choice_idx]
            break
        else:
            print("Invalid choice, please select a valid number.")
    except ValueError:
        print("Invalid input, please enter a number.")

config = MODEL_CONFIG[MODEL_CHOICE]

# Set the PERSIST_DIR based on the selected model
PERSIST_DIR = f"storage_{MODEL_CHOICE.lower()}"
article_directory = DATA_DIRECTORY

# Configure the settings
Settings.embed_model = HuggingFaceEmbedding(model_name=config["embed_model"],)
# Settings.embed_model = OpenAIEmbedding()

Settings.llm = HuggingFaceLLM(
    model_name=config["model_name"],
    tokenizer_name=config["tokenizer_name"],
    context_window=config["context_window"],
    max_new_tokens=config["max_new_tokens"],
    generate_kwargs=config["generate_kwargs"],
    # messages_to_prompt=messages_to_prompt_llama3,
    # completion_to_prompt=completion_to_prompt_llama3,
    # model_kwargs={"trust_remote_code": True},
    device_map="auto",  # try to force this to cuda.
)

index = create_or_load_index(PERSIST_DIR, article_directory)
rerank = SentenceTransformerRerank(
    model="BAAI/bge-reranker-large", top_n=5  # Note here
)

query_engine = index.as_query_engine(streaming=True, similarity_top_k=1, node_postprocessors=[rerank])


def chatbot_response(message, context_window, max_new_tokens, temperature, top_k, top_p):
    Settings.llm.context_window = context_window
    Settings.llm.max_new_tokens = max_new_tokens
    Settings.llm.generate_kwargs = {"temperature": temperature, "top_k": top_k, "top_p": top_p, "do sample": True}
    response = query_engine.query(message)
    return str(response)


iface = gr.Interface(
    fn=chatbot_response,
    inputs=[
        gr.Textbox(label="Message"),
        gr.Slider(minimum=512, maximum=4096, step=256, value=2048, label="Context Window"),
        gr.Slider(minimum=32, maximum=512, step=32, value=256, label="Max New Tokens"),
        gr.Slider(minimum=0.1, maximum=1.0, step=0.1, value=0.7, label="Temperature"),
        gr.Slider(minimum=1, maximum=100, step=1, value=50, label="Top K"),
        gr.Slider(minimum=0.5, maximum=1.0, step=0.05, value=0.95, label="Top P"),
    ],
    outputs=gr.Textbox(label="Response"),
    title="UESP Lore Chatbot",
    description="Ask questions about The Elder Scrolls lore!",
)

if __name__ == "__main__":
    iface.launch()
