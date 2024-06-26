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
   - Note that each vector store can currently hold a maximum of 500 files. It's recommended to consolidate related data into a master JSON file when necessary.

### Script: `attach_vector_stores_to_assistant.py`

This script is designed to help you set up your lore bot using data from a series of JSON files dedicated to specific topics. Each book is nested under its relevant topic.

**Example:**
- `religion_legends.json` contains books such as:
  - The Lunar Lorkhan
  - Sithis
  - Spirit of Nirn
  - And many more

For details on the structure of a book, see the `cleaning` section.

### Usage
1. Change the directory path in the script to match where you saved the data from this [link](https://app.mediafire.com/25peu9ki4zab5).
2. Run the script to attach the vector stores to your assistant.
3. Go to your Project dashboard, navigate to Assistants, and start enjoying your lore bot.