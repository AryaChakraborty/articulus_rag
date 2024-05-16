# get the huggingface token
import os
import subprocess
import sys
# import PDF loader
from langchain_community.document_loaders.pdf import PyPDFLoader
# import text splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
# import fast embeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# import vector store
from langchain.vectorstores import Chroma
# import the question-answering chain and Huggingface Hub LLM
from langchain.llms import HuggingFaceHub
# chains and prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

try:
    import streamlit as st
except ImportError:
    user_agree = input("The feature you're trying to use requires an additional library(s):streamlit. Would you like to install it now? [y/N]: ")
    if user_agree.lower() == 'y':
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        import streamlit as st
    else:
        raise ImportError("The required 'streamlit' is not installed.")
    
st.title("Chat with files")

# HuggingfaceHub Access Token
st.text("Enter HuggingfaceHub Access Token")
hf_token = st.text_input("HuggingfaceHub Access Token:", type="password")
os.environ['HUGGINGFACEHUB_API_TOKEN'] = hf_token

if hf_token:
    st.success("Huggingface Access token entered successfully!")
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

    if uploaded_file is not None:
        st.success("file uploaded successfully!")

        query = st.text_input("Enter your question")

        if query is not None:
            save_path = "./uploaded_files" # change this to your desired path or leave it as is
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            file_path = os.path.join(save_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # load the document
            loader = PyPDFLoader(file_path)
            data = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 512,
                chunk_overlap  = 0,
            )
            chunks = text_splitter.split_documents(data)

            model_name = "thenlper/gte-large"
            embedding_model = FastEmbedEmbeddings(model_name=model_name)

            # initialize the vector store (save to disk)
            db = Chroma.from_documents(chunks, embedding_model, 
                                       persist_directory="./chroma_db")

            # retrieve from vector db (load from disk) with query
            db2 = Chroma(persist_directory="./chroma_db", 
                         embedding_function=embedding_model)

            # initialize the retriever
            retriever = db2.as_retriever(
                search_type="mmr", #similarity
                search_kwargs={'k': 4}
            )

            # define the llm
            llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                                 model_kwargs={
                                     "temperature":0.1,
                                     "max_new_tokens":512,
                                     "return_full_text":False,
                                     "repetition_penalty":1.1,
                                     "top_p":0.9
                                    })

            template = """
            <s>[INST]
            You are an AI Assistant that follows instructions extremely well.
            Please be truthful and give direct answers. Please tell 'I don't know' if user query is not in CONTEXT
            [/INST]
            CONTEXT: {context}
            </s>
            [INST]
            {query}
            [/INST]
            """

            prompt = ChatPromptTemplate.from_template(template)

            output_parser = StrOutputParser()

            chain = (
                {"context": retriever, "query": RunnablePassthrough()}
                | prompt
                | llm
                | output_parser
            )

            response = chain.invoke(query)
            st.write(response)