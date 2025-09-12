import os
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request

from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.helper import download_embeddings
from src.propmt import system_prompt

# Setup the environemnt

try:
    load_dotenv()
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not PINECONE_API_KEY or not OPENAI_API_KEY:
            raise ValueError("Missing API keys in environment variables.")

    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    logging.info("API keys loaded successfully.")

except Exception as e:
    logging.error(f"Error loading environment variables: {e}")
    raise

# App Initialization

app = Flask(__name__)

# Lanchain SetUp

try:

    index_name = "finance-chatbot"
    embeddings = download_embeddings()

    # Embeded each chunk and upsert the embeddings into the Pinecode index
    docsearch = PineconeVectorStore.from_existing_index(
        index_name = index_name,
        embedding = embeddings
    )
    retriever = docsearch.as_retriever(
        search_type="similarity",
        search_kwargs={"k":3}
    )
    llm_chatmodel = ChatOpenAI(model="gpt-4o")

    prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
            ])

    question_answer_chain = create_stuff_documents_chain(llm_chatmodel,prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    logging.info("LangChain components initialized successfully.")

except Exception as e:
    logging.error(f"Error initializing LangChain components: {e}")
    raise

# Routes

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=['GET', 'POST'])
def chat():
    try:
        msg = request.form['msg']
        logging.info(f"Received message: {msg}")
        input = msg
        print(input)
        response = rag_chain.invoke({"input": msg})
        logging.info(f"Generated response: {response}")
        return str(response["answer"])
    except Exception as e:
        logging.error(f"Error during chat processing: {e}")
        return jsonify({"error": "Something went wrong. Please try again later."}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)