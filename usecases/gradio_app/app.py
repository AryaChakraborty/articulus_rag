import os
import sys
import shutil
import gradio as gr
from beyondllm import generator
from beyondllm.llms import GeminiModel

# Adding the directory of the script to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'streamlit_app'))
import ingest

upload_file_path = ""
def upload_file(file):  
    global upload_file_path  
    UPLOAD_FOLDER = "./uploaded_files"    
    if not os.path.exists(UPLOAD_FOLDER):    
        os.mkdir(UPLOAD_FOLDER)    
    shutil.copy(file, UPLOAD_FOLDER)    
    gr.Info("File Uploaded!!!")
    
    upload_file_path = file.name
    print(upload_file_path)
        

def process_query(google_api_key, vectordb_type, question, file_type, pinecone_api_key=None, pinecone_index_name=None, pinecone_option=None, pinecone_embedding_dim=768, pinecone_metric='cosine', pinecone_cloud='aws', pinecone_region=None):
    if google_api_key:
        os.environ['GOOGLE_API_KEY'] = google_api_key
        uploaded_file = os.path.basename(upload_file_path)
        if vectordb_type == 'Pinecone':
            retriever = ingest.get_retriever(
                                             uploaded_file,
                                             google_api_key, 
                                             vector_db=vectordb_type.lower(), 
                                             pinecone_api_key=pinecone_api_key, 
                                             pinecone_index_name=pinecone_index_name, 
                                             pinecone_option=pinecone_option,
                                             pinecone_embedding_dim=pinecone_embedding_dim,
                                             pinecone_metric=pinecone_metric,
                                             pinecone_cloud=pinecone_cloud,
                                             pinecone_region=pinecone_region,
                                             file_type=file_type,
                                             grCond=True)
        elif vectordb_type == 'Chroma':
            retriever = ingest.get_retriever( 
                                            uploaded_file,
                                             google_api_key, 
                                             vector_db=vectordb_type.lower(),
                                             file_type=file_type,
                                             grCond=True)
            
        llm = GeminiModel(model_name="gemini-pro",
                          google_api_key=os.environ.get('GOOGLE_API_KEY'))
        system_prompt = "You are an AI assistant, who answers questions based on uploaded files. You can answer anything about the data."
        pipeline = generator.Generate(question=question,
                                      retriever=retriever, 
                                      llm=llm, 
                                      system_prompt=system_prompt)
        response = pipeline.call()
        return response
    else:
        return "Please enter a valid Google API Key."

def gradio_app():
    with gr.Blocks() as demo:
        gr.Markdown("# Chat with Files")
        with gr.Row():
            google_api_key = gr.Textbox(label="Google API Key", type="password", placeholder="Enter Google API Key")
            vectordb_type = gr.Dropdown(choices=["Chroma", "Pinecone"], label="Select VectorDB Type", value="Chroma")
        pinecone_api_key = gr.Textbox(label="Pinecone API Key", type="password", placeholder="Enter Pinecone API Key", visible=False)
        pinecone_index_name = gr.Textbox(label="Pinecone Index Name", placeholder="Enter Pinecone Index Name", visible=False)
        pinecone_option = gr.Radio(choices=["Existing", "Create New"], label="Pinecone Option", visible=False)
        pinecone_embedding_dim = gr.Slider(minimum=1, maximum=2048, value=768, step=1, label="Embedding Dimension", visible=False)
        pinecone_metric = gr.Dropdown(choices=["cosine", "euclidean"], label="Metric", value="cosine", visible=False)
        pinecone_cloud = gr.Dropdown(choices=["aws", "gcp", "azure"], label="Cloud", value="aws", visible=False)
        pinecone_region = gr.Textbox(label="Region", placeholder="Enter Pinecone Region", visible=False)
        file_type = gr.Dropdown(choices=["csv", "pdf", "doc", "docx"], label="Select File Type", value="csv")
        
       
        upload_btn = gr.UploadButton("Click to Upload a File") 
        upload_btn.upload(upload_file, upload_btn)

        question = gr.Textbox(label="Enter your question")
        answer = gr.Textbox(label="Answer")
        submit_btn = gr.Button("Submit")
        submit_btn.click(fn=process_query, inputs=[google_api_key, vectordb_type, question, file_type, pinecone_api_key, pinecone_index_name, pinecone_option, pinecone_embedding_dim, pinecone_metric, pinecone_cloud, pinecone_region], outputs=[answer], show_progress=True)
        vectordb_type.change(fn=lambda x: gr.update(visible=x=="Pinecone"), inputs=[vectordb_type], outputs=[pinecone_api_key, pinecone_index_name, pinecone_option, pinecone_embedding_dim, pinecone_metric, pinecone_cloud, pinecone_region])

    demo.launch()

if __name__ == "__main__":
    gradio_app()
    