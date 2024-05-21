## Description of `app.py` 

### `app.py`

The `app.py` file contains the main application logic for gradio that allows users to upload files (such as CSV, PDF, DOC, or DOCX) and ask questions related to the content of those files. Here's an overview of its functionality:

1. **Imports:** The file starts with importing necessary libraries, including `streamlit` for building the web interface.

3. **File Upload and Question Input:** The user can input their Google API Key, choose a file type, upload a file, and enter a question related to the uploaded file. `os` and  `shutil` libraries are used for saving the uploaded files on local device and updates the `upload_file_path`.

4. **Retriever Initialization:** Depending on the chosen vector database type (`Chroma` or `Pinecone`), the appropriate retriever is initialized by the `process_query()` to extract relevant information from the uploaded file.

5. **LLM Initialization:** The GeminiModel is initialized to generate responses based on the uploaded file's content and the user's question.

6. **Response Generation:** Using the initialized retriever and LLM, the script generates a response to the user's question based on the uploaded file's content.

7. **Display Response:** The generated response is displayed to the user.


## Usage

1. Make sure you've installed pre-requisites from `pip install -r requirements.txt`
1. Run the Python script: `gradio app.py`
2. The Gradio application will open in your default web browser at `http://127.0.0.1/7860`.
3. Enter the required information (Google API Key, Vector Database Type, File Type) and upload a file.
4. If you selected Pinecone, provide the additional Pinecone-specific details.
5. Enter your question and click the "Submit" button.
6. The application will process the query and display the answer in the designated text box.

**Note:** There might be some error while retrieving the data in some cases, so try reloading the page and querying again.