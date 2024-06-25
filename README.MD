




  
  

# Elder Scrolls Lore Chatbot

This project utilizes `llamaindex` on top of `ChatGPT-3.5` or a local `ollama` install to enable users to ask questions about Elder Scrolls lore. It references a list of 7,000 topics from the UESP wiki, specifically those under the "Lore" designation.

The Hugging Faces Demo uses [Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) with BGE embeddings. The huggingfaces demo is being constantly updated until I can get a good balance of quality and speed. It is not very good compared to the local models. 

[Hugging Faces Demo](https://huggingface.co/spaces/emarron/elderscrolls_lore_bot)

Read below for more information about the system in general, or skip to the TIER LIST for the list of model/indexes pairs and my opinion on them.

This is not a chat system with extensive memory, so once you move to a new question, it usually won't remember your previous query.

These indexes are designed to answer questions about Elder Scrolls Lore, not to create new content. However, they can occasionally generate new ideas if prompted in the right way.

Please take everything generated with a **grain of salt**. 

To understand what I am specifically offering it's **VECTOR EMBEDDINGS**. This diagram should help.

The top is a normal path.

The second is using vector embeddings.

The bottom is a more detailed explanation while also still being simple.

For more info than that just search "LLM vector embeddings what are they?"

![](https://github.com/emarron/UESP-lore/blob/master/How%20Vector%20Embeddings%20Work.drawio.png?raw=true)

# Example:

### **Lore Question:**

This is using the chatgpt 3.5 turbo + ada embeddings of the 7,000 UESP articles.

**Prompt:** how does chim relate to dragonbreak

**Response:** CHIM is a state of enlightenment in the Elder Scrolls lore where one realizes the true nature of the universe and their place within it. It is achieved by understanding the illusory nature of reality and asserting one's individuality within that illusion. CHIM is said to grant individuals god-like powers, allowing them to manipulate reality. In the context of Dragon Breaks, CHIM is sometimes associated with the ability to maintain individuality and coherence during the chaotic and non-linear time of a Dragon Break. Some believe that those who have achieved CHIM may be able to navigate and even influence events during a Dragon Break due to their understanding of the true nature of existence.

###  **Asking for a story:**

 **Prompt:** write me a story about a dunmer overcoming skooma
 
**Response:** A Dunmer named Tilse Sendas shared her personal journey of overcoming skooma addiction. She described the initial infatuation, the intense obsession, and the deep degradation caused by her addiction. Through her narrative, Tilse revealed that the key to breaking free from the shackles of skooma lay in understanding and accepting the allure of the drug, as well as letting go of the shame associated with it. She emphasized that there was no magical cure or potion, but rather a path of self-awareness and choice. Tilse's story challenged the common belief that once enslaved by skooma, one could never break free, proving that redemption was possible through self-empowerment and a shift in perspective.

**human conclusion:** you might want to go check the wiki because that sure sounds like a book. Check the name Tilse Sendas. You will find this book: https://en.uesp.net/wiki/Lore:Confessions_of_a_Skooma-Eater


### **Asking for a story by combining the two prompts:**

**prompt:** "write me a story about Tilse Sendas while high on skooma achieving chim"

**response:** "Tilse Sendas, under the influence of skooma, embarked on a journey of self-discovery that led her to the elusive state of CHIM. As the moon-sugar coursed through her veins, she found herself in a realm where reality and illusion intertwined seamlessly. In her heightened state of consciousness, she delved deep into the mysteries of the universe, unraveling the secrets of existence and the nature of the divine.

Through the haze of skooma-induced euphoria, Tilse experienced profound insights and revelations that transcended mortal understanding. She danced on the edge of madness and enlightenment, teetering between oblivion and apotheosis. In a moment of clarity amidst the chaos, she grasped the essence of CHIM - the realization of the self within the dream of the Godhead.

With newfound clarity and purpose, Tilse Sendas embraced the divine spark within her being, achieving CHIM in a blaze of transcendent glory. In that fleeting moment of enlightenment, she became one with the universe, a radiant beacon of divine wisdom and power. And as the echoes of her enlightenment reverberated through the fabric of reality, Tilse Sendas ascended to a higher plane of existence, forever transformed by the profound truth she had uncovered in her skooma-induced revelation."

**human conclusion:** Yep that sure sounds like the elder scrolls.

## TIER LIST:


1. ChatGPT version works the best and is fastest. However, you need an API key and maybe 1 USD. 
2. Local Ollama is about the same as the Hugging Faces version (uses a flavor of Llama3) and can get slow if you don't have a GPU hooked up with torch (or a low power GPU).
3. Hugging Faces (Meta-Llama-3-8B-Instruct) is the easiest to use and has no requirements for hardware. 
4. Alternative Models: Qwen2-1-5b, Tinyllama-1, phi3-mini. These should only be used in a case where you have a lack of space. Qwen2 is okayish, Tinyllama is not good, Phi3 is a pain to get to run without a docker container.

### Examples of Same Query

This will consist of comparing **regular chatgpt** versus various embeddings + models.  All embeddings are referencing the same corpus (articles).

Structure is python file/other (Model + embedding system)

**Regular ChatGPT:**
**ChatGPT-3.5:**
- **Time:** 1s

-  **Prompt:** Who is Zarphus?

-  **Response:** Zarphus doesn't appear to be a widely recognized figure or entity in history, mythology, or popular culture based on available information. If you have more context or details about Zarphus, I could try to provide a more specific answer!


**Embedded Models Start:**
**Hugging Faces (Meta-Llama-3-8B-Instruct + BGE)**
- **Time:** 10-20s

-  **Prompt:** Who is Zarphus?

-  **Response:** Zaraphus was a Demi-Lich who possessed a special diamond that had several magical properties including the ability to show the owner the location of the Crystal Tower. It is unknown how Zaraphus obtained this gem but he was relieved of it when he was defeated in fair combat by the Mages Guild Loremaster Corim Ashlen.


**llama_indexer_chatgpt.py (chatgpt 3.5 + ada):**
- **Boot time:** 1~ minute. CPU usage mild during boot.
-  **RAM**: 1GB
- **Time:** 1.6s

-  **Prompt:** Who is Zarphus?

-  **Response:** Zaraphus was a Demi-Lich who possessed a special diamond with magical properties, including the ability to show the owner the location of the Crystal Tower. He lost this gem when he was defeated in fair combat by the Mages Guild Loremaster Corim Ashlen.

**llama_indexer_local_ollama.py (Ollama llama3 + BGE):**
- **Boot time:** 1~ minute. CPU usage mild during boot.
-  **RAM**: 1GB
-  **VRAM**: Can go up to 6-7GB in my tests. If you don't have that much VRAM force it to RAM. Uses some black magic to not consume 32GB.

- **Time:** 4s

-  **Prompt:** Who is Zarphus?

-  **Response:** Zaraphus was a Demi-Lich who possessed a special diamond that had several magical properties including the ability to show the owner the location of the Crystal Tower. It is unknown how Zaraphus obtained this gem but he was relieved of it when he was defeated in fair combat by the Mages Guild Loremaster Corim Ashlen.


## Getting Started

  

### Prerequisites

- A ChatGPT API key for chatgpt version - See step 4.
- Ollama installed for local_ollama - See step 4.
- HuggingFaces API key + Permissions for certain alternative models. This is for advanced users.

- Python 3.8 or higher

- Dependencies listed below

  

### Installation
  

1.  **Clone the Repository**

  

```bash

git clone https://github.com/your-repo/elder-scrolls-lore-chatbot.git

cd elder-scrolls-lore-chatbot

```

  

2.  **Download Storage Folder**

I have put in safeguards to prevent you from using the wrong index for different models. Each model needs a distinct index.
  
CHATGPT:
Download the storage folder from [\[Here\]](https://www.mediafire.com/file/zr9yl4n5s044c1s/storage_ada_chatgpt.7z/file) and place it in the project root directory.

OLLAMA:
Download the storage folder from [\[Here\]](https://www.mediafire.com/file/d210ifr8huhhrua/storage_bge-large-en-v1-5_local_ollama_llama3.7z/file) and place it in the project root directory.


3.  **Install Dependencies**

  

```bash

pip install -r requirements.txt

```

If you are using some of the alternative models you may need additonal dependencies. Further if you want to utilize your GPU you need [CUDA](https://developer.nvidia.com/cuda-toolkit) and [pytorch built for CUDA](https://pytorch.org/get-started/locally/).

4. **Download Ollama (local_ollama ONLY)**

If using the local version you need Ollama: [\[Here\]](https://ollama.com/download)
  

4.  **Set Up Environment Variables (CHATGPT and Alternatives)**

  

Create a `.env` file in the project root and add your ChatGPT API key and/or Hugging Faces API key:

  

```env

CHATGPT_API_KEY=your_api_key_here
HF_KEY=your_huggingfaces_api_key_here

```
The Hugging Faces key **might** be required for Alternative versions, but I don't know, you shouldn't use it anyway.

  

### Project Structure

-  `llama_indexer_local_ollama.py`: This is the local version, and it is slow but free.
-  `llama_indexer_chatgpt.py`: This is the chatgpt version which is also more or less free unless you make a lot of requests to chatgpt.
- `llama_indexer_hf_type.py`: Where the aforementioned alternative versions are. This is an experimental file and uses the `requirements_full.txt`.-  `cleaning_HTML directory`: Cleans HTML data, requires `beautifulsoup4`.

-  `cleaning_ARTICLES directory`: Further processing and cleaning of articles.

-  `cleaning_TESCONV_JSON directory`: Processes JSON dumps of game data from TES3CONV. Note: This section is less polished. No I cannot provide game dumps. You can get these easily with [TES3CONV](https://github.com/Greatness7/tes3conv)

-  `failures`: Contains attempts to create an independent small LLM or LoRA that were unsuccessful due to being not good or taking forever.

- `chatbot resources`: contains resource python files
- `model configs`: contains configs for hugging faces sourced models.
  

### Optional Data

  

-  **HERE**: [\[Download link\]](https://app.mediafire.com/x3nhxfhn1m3o1)

**DATA**: All of these contain over 7,000 articles.
- articles: the training set as json
- UESP_LORE_DUMP: raw html from the UESP wiki where page was present in [Lore](https://en.uesp.net/wiki/Special:AllPages?from=&to=&namespace=130&hideredirects=1). 
- IMPERIAL_LIBRARY_DUMP: raw html from the imperial library

**EMBEDDINGS**: storage_(EMBEDDING_METHOD)_(LLM):
- storage_ada_gpt_3-5-turbo: this is for the chatgpt version
- storage_bge-base-en-v1-5_local_llama3: this is for the local ollama version
- storage_bge-base-en-v1-5_Meta-Llama-3-8B-Instruct: Hugging Faces is using this one.
- storage_bge-base-en-v1-5_TinyLlama-1-1B-Chat-v1-0: For TinyLlama 1B Chat
- storage_bge_base_en_v1-5_Phi-3-mini-128k-instruct: For Phi-3-mini 128k instruct
- storage_bge_base_en_v1-5_Qwen2-1-5B-Instruct: For Qwen2 1.5B instruct

At later dates I may revise these embeddings by changing the dataset. Currently I am working on implementing a tagging system.
### Usage

  

1.  **Run the Llama Indexer**

  

If there is no data in the storage folder but there is data in the articles folder, the script will train the model. Otherwise, it will start the chatbot. Most likely you want the chatbot so scroll up and download the storage.

  

```bash

python llama_indexer_chatgpt.py

```
 or 
```bash

python llama_indexer_local_ollama.py

```

After a bit of processing the terminal will pop up with a 

```
Running on local URL:  http://127.0.0.1:7860
```

Simply click the URL to be taken to a chat window.

2.  **Ask Questions**

  

Interact with the chatbot to get answers about Elder Scrolls lore. I would advise cross-referencing the result with UESP. You can also ask it silly stuff like this.

  

**You**: Write me a poem about Zaraphus

**Chatbot**: Zaraphus, the Demi-Lich of old,
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
