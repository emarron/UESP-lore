


  
  

# Elder Scrolls Lore Chatbot

  

This project utilizes `llamaindex` on top of `ChatGPT-3.5` or a local `ollama` install to enable users to ask questions about Elder Scrolls lore. It references a list of 7,000 topics from the UESP wiki. Specifically that which were under the designation "Lore".

If you hate installing stuff you can try this when it actually starts working (Its very slow):
  
[HuggingFaces Demo](https://huggingface.co/spaces/emarron/elderscrolls_lore_bot
)

This is not a chat system with a lot of memory so as soon as you move to a new question, it won't remember your previous query (usually).

In general I am highly satisfied with the ChatGPT version, satisfied with the local Ollama, not happy with tinyllama, and very disappointed in the huggingfaces (tinyllama) version.

These models are for answering questions about Elder Scrolls Lore not coming up with new stuff although they can occasionally do that if you poke it in the right way.

 I would advise everything to be taken **with a grain of salt**, and these models should be used as a tool to more efficiently browse for elder scrolls lore. It's not really for generating new content but answering questions you may have.
 

**e.g: Lore Question:**

**prompt:** how does chim relate to dragonbreak

**response:** CHIM is a state of enlightenment in the Elder Scrolls lore where one realizes the true nature of the universe and their place within it. It is achieved by understanding the illusory nature of reality and asserting one's individuality within that illusion. CHIM is said to grant individuals god-like powers, allowing them to manipulate reality. In the context of Dragon Breaks, CHIM is sometimes associated with the ability to maintain individuality and coherence during the chaotic and non-linear time of a Dragon Break. Some believe that those who have achieved CHIM may be able to navigate and even influence events during a Dragon Break due to their understanding of the true nature of existence.

 **e.g asking for a story:**

 **prompt:** "write me a story about a dunmer overcoming skooma"
 
**response:** "A Dunmer named Tilse Sendas shared her personal journey of overcoming skooma addiction. She described the initial infatuation, the intense obsession, and the deep degradation caused by her addiction. Through her narrative, Tilse revealed that the key to breaking free from the shackles of skooma lay in understanding and accepting the allure of the drug, as well as letting go of the shame associated with it. She emphasized that there was no magical cure or potion, but rather a path of self-awareness and choice. Tilse's story challenged the common belief that once enslaved by skooma, one could never break free, proving that redemption was possible through self-empowerment and a shift in perspective."

**human conclusion:** you might want to go check the wiki because that sure sounds like a book. Check the name Tilse Sendas.

**wiki result:** https://en.uesp.net/wiki/Lore:Confessions_of_a_Skooma-Eater

finally

**e.g asking for a story based on the last two prompts:**

**prompt:** "write me a story about Tilse Sendas while high on skooma achieving chim"

**response:** "Tilse Sendas, under the influence of skooma, embarked on a journey of self-discovery that led her to the elusive state of CHIM. As the moon-sugar coursed through her veins, she found herself in a realm where reality and illusion intertwined seamlessly. In her heightened state of consciousness, she delved deep into the mysteries of the universe, unraveling the secrets of existence and the nature of the divine.

Through the haze of skooma-induced euphoria, Tilse experienced profound insights and revelations that transcended mortal understanding. She danced on the edge of madness and enlightenment, teetering between oblivion and apotheosis. In a moment of clarity amidst the chaos, she grasped the essence of CHIM - the realization of the self within the dream of the Godhead.

With newfound clarity and purpose, Tilse Sendas embraced the divine spark within her being, achieving CHIM in a blaze of transcendent glory. In that fleeting moment of enlightenment, she became one with the universe, a radiant beacon of divine wisdom and power. And as the echoes of her enlightenment reverberated through the fabric of reality, Tilse Sendas ascended to a higher plane of existence, forever transformed by the profound truth she had uncovered in her skooma-induced revelation."

**human conclusion:** Yep that sure sounds like the elder scrolls.

### TIER LIST:

1. ChatGPT version as it works the best and it is the fastest. I think you can have a chatGPT API key for free so why not.
2. Local Ollama is not as good as chatgpt and can get slow if you don't have a GPU hooked up with torch (or a low power GPU).
3. Local TinyLlama is here just because I have it, it's the local version of the Hugging Faces Demo.
4. Hugging faces demo is to see if you like the general vibe. It's very... not good.
### Examples of Same Query

**ChatGPT-3.5:**
- **Time:** 1s

-  **Prompt:** Who is Zarphus?

-  **Response:** Zarphus doesn't appear to be a widely recognized figure or entity in history, mythology, or popular culture based on available information. If you have more context or details about Zarphus, I could try to provide a more specific answer!

  

**llama_indexer_chatgpt.py:**
- **Time:** 1.6s

-  **Prompt:** Who is Zarphus?

-  **Response:** Zaraphus was a Demi-Lich who possessed a special diamond with magical properties, including the ability to show the owner the location of the Crystal Tower. He lost this gem when he was defeated in fair combat by the Mages Guild Loremaster Corim Ashlen.

**llama_indexer_local_ollama.py:**
- **Time:** 4s

-  **Prompt:** Who is Zarphus?

-  **Response:** Zaraphus was a Demi-Lich who possessed a special diamond that had several magical properties including the ability to show the owner the location of the Crystal Tower. It is unknown how Zaraphus obtained this gem but he was relieved of it when he was defeated in fair combat by the Mages Guild Loremaster Corim Ashlen.


**llama_indexer_local_tinyllama.py:**
- **Time:** 8.7s
-  **Prompt:** Who is Zarphus?
- **Response:** Zarphus (fl. before 3E 389) was a Demi-Lich who possessed a special diamond that had several magical properties including the ability to show the owner the location of the Crystal Tower . It is unknown how Zarphus obtained this gem but he was relieved of it when he was defeated in fair combat by the Mages Guild Loremaster Corim Ashlen . [1] Mane Zebiden-jo (fl. ~ 2E 182 ) [ edit ] Zebiden-jo (or Zibbiden-jo ) was the Mane of the Khajiiti people during the early Second Era , before the unification of the Sixteen Kingdoms. Little is known about Zebiden-jo's life. It is known, however, that he faced one of his parent's spirit and Argonian soul reavers during his trials to become the Mane circa 2E 182 . The trials reflected the challenges faced before their ascension. He died at some point before the unification of Elsweyr and formation of the Elsweyr Confederacy in 2E 309 . His remains

**Hugging Faces which uses llama_indexer_local_tinyllama.py**
- **Time:** 170s

-  **Prompt:** Who is Zarphus?

-  **Response:** Zarphus (fl. before 3E 389) [ edit ] Zarphus was a Demi-Lich who possessed a special diamond that had several magical properties including the ability to show the owner the location of the Crystal Tower . It is unknown how Zarphus obtained this gem but he was relieved of it when he was defeated in fair combat by the Mages Guild Loremaster Corim Ashlen . [1] Mane Zebiden-jo (fl. ~ 2E 182 ) [ edit ] Zebiden-jo (or Zibbiden-jo ) was the Mane of the Khajiiti people during the early Second Era , before the unification of the Sixteen Kingdoms. Little is known about Zebiden-jo's life. It is known, however, that he faced one of his parent's spirit and Argonian soul reavers during his trials to become the Mane circa 2E 182 . The trials reflected the challenges faced before their ascension. He died at some point before the unification of Elsweyr and formation of the Elsweyr Confederacy in 2E 


## Getting Started

  

### Prerequisites

- A ChatGPT API key for chatgpt version - See step 4.
- Ollama installed for local_ollama - See step 4.
- (maybe) HuggingFaces API key for local_tinyllama - See step 4.

- Python 3.8 or higher

- Dependencies listed below

  

### Installation
  

1.  **Clone the Repository**

  

```bash

git clone https://github.com/your-repo/elder-scrolls-lore-chatbot.git

cd elder-scrolls-lore-chatbot

```

  

2.  **Download Storage Folder**

  
CHATGPT:
Download the storage folder from [\[Here\]](https://www.mediafire.com/file/0awjd9hcds0dg7e/storage_ada_gpt_3-5-turbo.7z/file) and place it in the project root directory.

OLLAMA:
Download the storage folder from [\[Here\]](https://www.mediafire.com/file/nc1wxmdwzje4j6t/storage_bge-base-en-v1-5_local_llama3.7z/file) and place it in the project root directory.

TINYLLAMA:
Download the storage folder from [\[Here\]](https://www.mediafire.com/file/5o5k3wmehvhacoc/storage_bge-base-en-v1-5_TinyLlama-1-1B-Chat-v1-0.7z/file) and place it in the project root directory.


  

3.  **Install Dependencies**

  

```bash

pip install -r requirements.txt

```

4. **Donwload Ollama (local_ollama ONLY)**

If using the local version you need Ollama: [\[Here\]](https://ollama.com/download)
  

4.  **Set Up Environment Variables (CHATGPT and local_tinyllama ONLY)**

  

Create a `.env` file in the project root and add your ChatGPT API key and/or Hugging Faces API key:

  

```env

CHATGPT_API_KEY=your_api_key_here
HF_KEY=your_huggingfaces_api_key_here

```
The Hugging Faces key **might** be required for the TinyLlama version, but I don't know, you shouldn't use it anyway.

  

### Project Structure

-  `llama_indexer_local_ollama.py`: This is the local version, and it is slow but free.
-  `llama_indexer_chatgpt.py`: This is the chatgpt version which is also more or less free unless you make a lot of requests to chatgpt.
-  `llama_indexer_local_tinyllama.py` This is the worst version, and is somehow slower than local_ollama (at least on my machine).
-  `cleaning_HTML directory`: Cleans HTML data, requires `beautifulsoup4`.

-  `cleaning_ARTICLES directory`: Further processing and cleaning of articles.

-  `cleaning_TESCONV_JSON directory`: Processes JSON dumps of game data from TES3CONV. Note: This section is less polished. No I cannot provide game dumps. You can get these easily with [TES3CONV](https://github.com/Greatness7/tes3conv)

-  `failures`: Contains attempts to create an independent small LLM or LoRA that were unsuccessful due to being not good or taking forever.

  

### Optional Data

  

-  **HERE**: [\[Download link\]](https://app.mediafire.com/x3nhxfhn1m3o1)

**DATA**: All of these contain over 7,000 articles.
- articles: the training set as json
- articles_categorized: same thing as articles but just in subdirectories. e.g: People, Books, Places...
- UESP_LORE_DUMP: raw html from the UESP wiki where page was present in [Lore](https://en.uesp.net/wiki/Special:AllPages?from=&to=&namespace=130&hideredirects=1). 

**EMBEDDINGS**: storage_(EMBEDDING_METHOD)_(LLM):
- storage_ada_gpt_3-5-turbo: this is for the chatgpt version
- storage_bge-base-en-v1-5_local_llama3: this is for the local ollama version
- storage_bge-base-en-v1-5_Meta-Llama-3-8B-Instruct: this was for a hugging faces version, but it was too computationally expensive for the free gradio I'm using.
- storage_bge-base-en-v1-5_TinyLlama-1-1B-Chat-v1-0: this is the one paired with the hugging faces demo.
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
 or if you hate yourself
```bash

python llama_indexer_local_tinyllama.py

```

All of them will pop up with a 

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
