# Finance_Chatbot

### STEP 1:

Clone the repository

```bash
Project repo: https://github.com/Shihamfm/Finance_Chatbot.git

```
### STEP 2 - Create a virtual environment after opening the inventory

```bash
python -m venv finance_chatbot
```

```bash
source finance_chatbot/Scripts/activate
```

### STEP 3 - Install the requirements
```bash
pip install -r requirements.txt
```
## Create a .env file in the root directory and add the Pinecone & openai credentials as follows:
```bash
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
```bash
# run the following command to store embeddings to pinecone
python store_index.py
```

```bash
# Finally run the following command
python app.py
```
Now,
```base
open up localhost:
```
## Techstack Used:
- Python
- LangChain
- Flask
- GPT
- Pinecone


