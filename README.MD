

# Elder Scrolls Lore Chatbot

This project utilizes `llamaindex` on top of `ChatGPT-3.5` to enable users to ask questions about Elder Scrolls lore. It references a list of 7,000 topics from the UESP wiki. Specifically that which were under the designation "Lore".

### Example

**ChatGPT-3.5:**
- **Prompt:** Who is Zarphus?
- **Response:** Zarphus doesn't appear to be a widely recognized figure or entity in history, mythology, or popular culture based on available information. If you have more context or details about Zarphus, I could try to provide a more specific answer!

**llama_indexer.py:**
- **Prompt:** Who is Zarphus?
- **Response:** Zaraphus was a Demi-Lich who possessed a special diamond with magical properties, including the ability to show the owner the location of the Crystal Tower. He lost this gem when he was defeated in fair combat by the Mages Guild Loremaster Corim Ashlen.


## Getting Started

### Prerequisites

- A ChatGPT API key
- Python 3.8 or higher
- Dependencies listed below

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-repo/elder-scrolls-lore-chatbot.git
   cd elder-scrolls-lore-chatbot
   ```

2. **Download Storage Folder**

   Download the storage folder from [\[Here\]](https://www.mediafire.com/file/amooo5lm6jxwm2m/storage.7z/file) and place it in the project root directory.

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the project root and add your ChatGPT API key:

   ```env
   CHATGPT_API_KEY=your_api_key_here
   ```

### Project Structure

- `llama_indexer.py`: If data is present in the storage folder, it starts a chatbot that you can use to ask about Elder Scrolls lore. Otherwise it serves as a trainer if no data is in the storage folder but THERE IS data in the articles folder. 
- `cleaning_HTML directory`: Cleans HTML data, requires `beautifulsoup4`.
- `cleaning_ARTICLES directory`: Further processing and cleaning of articles.
- `cleaning_TESCONV_JSON directory`: Processes JSON dumps of game data from TESCONV. Note: This section is less polished. No I cannot provide game dumps.
- `failures`: Contains attempts to create an independent small LLM or LoRA that were unsuccessful due to being not good or taking forever.

### Optional Data

- **HTML Raw Data**: [\[Download link\]](https://www.mediafire.com/file/gwcvx4wn59c01q8/UESP_LORE_DUMP.7z/file)
- **Categorized Articles**: [\[Download link\]](https://www.mediafire.com/file/06i4q8pkxwrbh0i/articles_categorized.7z/file)
- **Articles Folder**: [\[Download link\]](https://www.mediafire.com/file/o66jcb5w64a12o0/articles.7z/file)

### Usage

1. **Run the Llama Indexer**

   If there is no data in the storage folder but there is data in the articles folder, the script will train the model. Otherwise, it will start the chatbot. Most likely you want the chatbot so scroll up and download the storage.

   ```bash
   python llama_indexer.py
   ```

2. **Ask Questions**

   Interact with the chatbot to get answers about Elder Scrolls lore. I would advise cross-referencing the result with UESP. You can ask it silly stuff like this.

   You: Write me a poem about Zaraphus
    Chatbot: Zaraphus, the Demi-Lich of old,
    With a diamond that shone like gold.
    His gem revealed the Crystal Tower's sight,
    Lost in fair combat, his powers took flight.

    Mages Guild Loremaster, Corim Ashlen's might,
    Defeated Zaraphus in the magical fight.
    A tale of power, of magic, and lore,
    Zaraphus, the Demi-Lich, forevermore.

### Contributing

Contributions are welcome! Please fork the repository and create a pull request.

### License

This project is licensed under the MIT License.