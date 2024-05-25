import os
import shutil
from beyondllm.retrieve import auto_retriever
from beyondllm.vectordb import ChromaVectorDb, PineconeVectorDb
from beyondllm.embeddings import GeminiEmbeddings
from beyondllm import source
from url import get_url_content
from urllib.parse import urlparse

def get_retriever(uploaded_file=None, url=None, 
                  google_api_key=None, 
                  vector_db='chroma', 
                  pinecone_api_key=None, 
                  pinecone_index_name=None, 
                  pinecone_option=None, 
                  pinecone_embedding_dim=None, 
                  pinecone_metric=None, 
                  pinecone_cloud=None, 
                  pinecone_region=None,
                  grCond = False,
                  file_type=None):
    
    if google_api_key:
        # Save the uploaded file or content from URL
        save_path = "./uploaded_files"  # change this to your desired path or leave it as is
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        file_path = None
        if uploaded_file:
            file_path = os.path.join(save_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        elif url:
            content = get_url_content(url)
            if content:
                parsed_url = urlparse(url)
                file_name = f"{parsed_url.netloc}.pdf"
                file_path = os.path.join(save_path, file_name)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
        
        if file_path:
            if uploaded_file:
                 # Fit the data
                 data = source.fit(file_path, dtype=file_type, chunk_size=512, chunk_overlap=50)
            elif url:
                data = source.fit(file_path, dtype='pdf', chunk_size=512, chunk_overlap=50)

            
            # Initialize your embedding model
            embed_model = GeminiEmbeddings(api_key=google_api_key, model_name="models/embedding-001")
            
            # Initialize your vector store
            if vector_db == 'chroma':
                vector_store = ChromaVectorDb(collection_name='my_persistent_collection', persist_directory='./db/chroma/')
            elif vector_db == 'pinecone':
                if pinecone_option == 'Existing':
                    # Initialize an existing Pinecone index
                    vector_store = PineconeVectorDb(index_name=pinecone_index_name)
                else:
                    # Create a new serverless Pinecone index
                    vector_store = PineconeVectorDb(
                        create=True,
                        api_key=pinecone_api_key,
                        index_name=pinecone_index_name,
                        embedding_dim=pinecone_embedding_dim,
                        metric=pinecone_metric,
                        cloud=pinecone_cloud,
                        region=pinecone_region,
                    )
            else:
                return None
            
            # Initialize the retriever
            retriever = auto_retriever(data=source.fit(file_path, dtype=file_type or 'pdf', chunk_size=512, chunk_overlap=50), embed_model=embed_model, type="normal", top_k=5, vectordb=vector_store)
            
            return retriever

    return None
