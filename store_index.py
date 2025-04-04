from src.helper import load_pdf_file, text_split, download_embedding_model
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
import joblib

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# extracted_data = load_pdf_file(data = 'Data/')
#rerun the above line to load the pdf files again if cache is cleared
# import joblib
# joblib.dump(extracted_data, 'cached_data.joblib')
#for caching the data
extracted_data = joblib.load('cached_data.joblib')
text_chunks=text_split(extracted_data)
embeddings = download_embedding_model()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalbot"


pc.create_index(
    name=index_name,
    dimension=384, 
    metric="cosine", 
    spec=ServerlessSpec(
        cloud="aws", 
        region="us-east-1"
    ) 
) 

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings, 
)