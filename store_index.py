from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"]= PINECONE_API_KEY

extracted_data=load_pdf_file(data="Data/")

text_chunks=text_split(extracted_data)

embeddings=download_hugging_face_embeddings()

pc= Pinecone(api_key="pcsk_KjGui_u2DMwk4MFrTyrqNupdE38uh3nk6wPePc3TNyPCPEJEceGxrHLyRJYzMduJLu6a")

index_name='medicalbot'

pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

#Enable each chunk and upsert the embedding into your Pinecone index.

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity",search_kwargs={"k":3})