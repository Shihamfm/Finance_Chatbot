import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings

load_dotenv()

#Setting the environment variable
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)

from pinecone import ServerlessSpec

index_name = "finance-chatbot"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384, #Equal to the dimension of the HuggingFace embedding model
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws", #Cosine similarity
            region="us-east-1"
        )
    )

embeddings = download_embeddings()
extracted_data = load_pdf_files("data")
filtered_docs = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filtered_docs)

docsearch = PineconeVectorStore.from_documents(documents = text_chunks,
                                                embedding = embeddings,
                                                index_name = index_name
                                                )
