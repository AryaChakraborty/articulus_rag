import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from beyondllm import source,retrieve,generator
from utils.mapping import url_map
from beyondllm.llms import GeminiModel
from beyondllm.embeddings import HuggingFaceEmbeddings
from utils.keywordExtractor import keyword_from_search_sentence
from utils.rankBlogs import rank_documents
from dotenv import load_dotenv # type: ignore
import pymongo as pym
load_dotenv()
from werkzeug.exceptions import HTTPException
from functools import wraps
import os

# configure logging and save the logs in a file within the logs directory
logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# get all the env variables
MONGO_URL = os.getenv("MONGO_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# connect to the mongodb database
client = pym.MongoClient(MONGO_URL)
db = client["newsgpt"]
blog_collection = db["articles"]
user_collection = db["users"]

# define the app
app = Flask(__name__)
CORS(app)

# Custom error handler
@app.errorhandler(Exception)
def handle_exception(e):
    # Handle HTTP exceptions
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    # Handle non-HTTP exceptions
    logging.error(f"Unhandled exception: {e}")
    return jsonify({"error": "Internal server error"}), 500

def validate_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Invalid input, expected JSON"}), 400
        return f(*args, **kwargs)
    return decorated_function

def sanitize_input(data):
    # Implement sanitization logic (e.g., escaping special characters)
    if isinstance(data, str):
        return data.replace("<", "&lt;").replace(">", "&gt;")
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_input(item) for item in data]
    return data

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the NewsGPT API!"

@app.route('/recommend', methods=['GET'])
def recommend_endpoint():
    '''
    calls the rank_documents function with the search keywords as an empty list and the documents and returns the ranked documents.
    '''
    try:
        # identifiers for the database and the collection
        documents = list(blog_collection.find({}))
        users = list(user_collection.find({}))
        search_keywords = []
        #Sanitize the documents and users
        documents = sanitize_input(documents)
        users = sanitize_input(users)

        # displaying all documents while sorting based on the search keywords.
        ranked_documents = rank_documents(search_keywords=search_keywords,
                                          documents=documents,
                                          users=users, 
                                          search_filter=False)
                                        
        # Create a list of ranked documents with their title, user, and slug                                  
        ranked_list = [{'title': doc[0], 'user': doc[1], 'slug': doc[2]} for doc in ranked_documents]
        return jsonify({"ranked_documents": ranked_list})
    except Exception as e:
        logging.error(f"Error in /recommend endpoint: {e}")
        return jsonify({"error": str(e)})

@app.route('/rank', methods=['POST'])
@validate_json
def rank_endpoint():
    '''
    calls the rank_documents function with the search keywords from the data and the documents and returns the ranked documents.
    '''
    try:
        data = sanitize_input(request.json)
        search_keywords = data.get('search_keywords')

        # Validate search_keywords
        if not isinstance(search_keywords, list):
            return jsonify({"error": "Invalid input, search_keywords should be a list"}), 400

        documents = list(blog_collection.find({}))
        users = list(user_collection.find({}))

        # Sanitize the documents and users
        documents = sanitize_input(documents)
        users = sanitize_input(users)
        # displaying all documents while sorting based on the search keywords.
        ranked_documents = rank_documents(search_keywords=search_keywords,
                                          documents=documents,
                                          users=users, 
                                          search_filter=True)
        ranked_list = [{'title': doc[0], 'user': doc[1], 'slug': doc[2], 'image': doc[3]} for doc in ranked_documents]
        return jsonify({"ranked_documents": ranked_list})
    except Exception as e:
        logging.error(f"Error in /rank endpoint: {e}")
        return jsonify({"error": str(e)})

@app.route('/keyword_extractor', methods=['POST'])
@validate_json
def yake_endpoint():
    '''
    takes data in the form of a dictionary with the key 'text' and returns the top 10 keywords from the text.
    '''
    try:
        data = sanitize_input(request.json)
        text = data.get('body')

        # Validate text
        if not isinstance(text, str):
            return jsonify({"error": "Invalid input, body should be a string"}), 400

        # Extract keywords from the provided text
        keywords = keyword_from_search_sentence(text)
        return jsonify({"keywords": keywords})
    except Exception as e:
        logging.error(f"Error in /keyword_extractor endpoint: {e}")
        return jsonify({"error": str(e)})

@app.route('/ai', methods=['POST'])
@validate_json
def ai_endpoint():
    '''
    takes data in the form of a dictionary with the keys 'path', 'type', and 'question' and returns the response from the enterprise RAG model.
    '''
    try:
        data_post = sanitize_input(request.json)
        path = url_map[data_post.get('path')] # https://highonbugs.sbk2k1.in/sows
           # Validate input
        if not path:
            return jsonify({"error": "Invalid input, path not found in url_map"}), 400

        # print(path)
        dtype = data_post.get('type') # "url", "youtube", etc.
        question = data_post.get('question') # What is the best way to learn python?
        if not isinstance(dtype, str) or not isinstance(question, str):
            return jsonify({"error": "Invalid input, 'type' and 'question' should be strings"}), 400


        data = source.fit(path=path,
                          dtype=dtype,
                          chunk_size=1024)
                          
        embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

        retriever = retrieve.auto_retriever(data=data,
                                            embed_model=embed_model,
                                            type="normal",
                                            top_k=3)

        llm = GeminiModel(model_name="gemini-pro",
                          google_api_key = GOOGLE_API_KEY)

        pipeline = generator.Generate(
                 question=question,
                 system_prompt = "you are a smart AI chatbot, answer the question asked by the user",
                 llm = llm,
                 retriever=retriever)
        
        response = pipeline.call()

        return jsonify({"response": response})
    
    except Exception as e:
        logging.error(f"Error in /ai endpoint: {e}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
