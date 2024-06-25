import gradio as gr
from dotenv import load_dotenv
from llama_index.core.postprocessor import SentenceTransformerRerank
from chat_bot_resources.config import DATA_DIRECTORY
from chat_bot_resources.resources import create_or_load_index

PERSIST_DIR = 'storage_chatgpt'
articles_directory = DATA_DIRECTORY

load_dotenv()

index = create_or_load_index(PERSIST_DIR, articles_directory)
rerank = SentenceTransformerRerank(
    model="BAAI/bge-reranker-large", top_n=5  # Note here
)
query_engine = index.as_query_engine(streaming=True, similarity_top_k=1, node_postprocessors=[rerank])


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
