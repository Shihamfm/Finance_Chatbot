# import libraries
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings


# Extract text from pdf files
def load_pdf_files(data):
    loader = DirectoryLoader(data,
                             glob="./*pdf",
                             loader_cls=PyPDFLoader
                             )
    documents = loader.load()
    return documents

# Filter the docs
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source'in metadata and original content
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source":src}
            )
        )
    return minimal_docs

# Split the docs into smaller chuck
def text_split(filtered_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    texts = text_splitter.split_documents(filtered_docs)
    return texts

#Embeddings
def download_embeddings():
    """
    Donwload and return the HuggingFace embeddings model.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
    )
    return embeddings