## README: ChatGPT Assistant

### Prerequisites
- OpenAI account with API access
- ChatGPT project with an assistant

### Resources
- [OpenAI API Reference: Vector Stores](https://platform.openai.com/docs/api-reference/vector-stores)
- [Tutorial Video](https://www.youtube.com/watch?v=JGMG1mXaY1c)

### Steps

1. **Set Up Project**
   - Create a ChatGPT project and an assistant in the OpenAI dashboard.

2. **Understand Vector Stores**
   - Vector stores enhance data retrieval using vector embeddings. Refer to the [API documentation](https://platform.openai.com/docs/api-reference/vector-stores).
    - An important limit is that each vector store can only have 500 files at this moment. I would recommend you consolidate related data to a master json.


This file 
`attach_vector_stores_to_assistant.py` is specifically designed to help you set up your lore bot.
It uses this [data](https://app.mediafire.com/25peu9ki4zab5).

Please change the directory path to match where you put this directory to hand the references to chatgpt.