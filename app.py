import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from beyondllm import source, retrieve, generator
from utils.mapping import url_map
from beyondllm.llms import GeminiModel
from beyondllm.embeddings import HuggingFaceEmbeddings
from utils.keywordExtractor import keyword_from_search_sentence
from utils.rankBlogs import rank_documents
from dotenv import load_dotenv  # type: ignore
import pymongo as pym
from marshmallow import Schema, fields, ValidationError  # Added for schema validation
import bleach  # Added for input sanitization
import os

load_dotenv()

# Configure logging and save the logs in a file within the logs directory
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get all the env variables
MONGO_URL = os.getenv("MONGO_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Connect to the MongoDB database
client = pym.MongoClient(MONGO_URL)
db = client["newsgpt"]
blog_collection = db["articles"]
user_collection = db["users"]

# Define the app
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the NewsGPT API!"

# Schema for validating /rank endpoint requests
class RankRequestSchema(Schema):
    search_keywords = fields.List(fields.Str(), required=True)

# Schema for validating /keyword_extractor endpoint requests
class KeywordExtractorSchema(Schema):
    body = fields.Str(required=True)

# Schema for validating /ai endpoint requests
class AIRequestSchema(Schema):
    path = fields.Str(required=True)
    type = fields.Str(required=True)
    question = fields.Str(required=True)

@app.route('/recommend', methods=['GET'])
def recommend_endpoint():
    try:
        documents = list(blog_collection.find({}))
        users = list(user_collection.find({}))
        search_keywords = []
        ranked_documents = rank_documents(
            search_keywords=search_keywords,
            documents=documents,
            users=users,
            search_filter=False
        )
        ranked_list = [{'title': doc[0], 'user': doc[1], 'slug': doc[2]} for doc in ranked_documents]
        return jsonify({"ranked_documents": ranked_list})
    except Exception as e:
        logging.error(f"Error in /recommend endpoint: {e}")
        return jsonify({"error": str(e)})

@app.route('/rank', methods=['POST'])
def rank_endpoint():
    try:
        data = request.json
        schema = RankRequestSchema()  # Create an instance of the schema
        result = schema.load(data)  # Validate incoming data against the schema
        search_keywords = [bleach.clean(keyword) for keyword in result['search_keywords']]  # Sanitize the validated keywords
        documents = list(blog_collection.find({}))
        users = list(user_collection.find({}))
        ranked_documents = rank_documents(
            search_keywords=search_keywords,
            documents=documents,
            users=users,
            search_filter=True
        )
        ranked_list = [{'title': doc[0], 'user': doc[1], 'slug': doc[2], 'image': doc[3]} for doc in ranked_documents]
        return jsonify({"ranked_documents": ranked_list})
    except ValidationError as err:
        logging.error(f"Validation error in /rank endpoint: {err}")  # Log validation errors
        return jsonify({"error": err.messages}), 400  # Return validation errors to the client
    except Exception as e:
        logging.error(f"Error in /rank endpoint: {e}")
        return jsonify({"error": str(e)})

@app.route('/keyword_extractor', methods=['POST'])
def yake_endpoint():
    try:
        data = request.json
        schema = KeywordExtractorSchema()  # Create an instance of the schema
        result = schema.load(data)  # Validate incoming data against the schema
        text = bleach.clean(result['body'])  # Sanitize the validated text
        keywords = keyword_from_search_sentence(text)
        return jsonify({"keywords": keywords})
    except ValidationError as err:
        logging.error(f"Validation error in /keyword_extractor endpoint: {err}")  # Log validation errors
        return jsonify({"error": err.messages}), 400  # Return validation errors to the client
    except Exception as e:
        logging.error(f"Error in /keyword_extractor endpoint: {e}")
        return jsonify({"error": str(e)})

@app.route('/ai', methods=['POST'])
def ai_endpoint():
    try:
        data_post = request.json
        schema = AIRequestSchema()  # Create an instance of the schema
        result = schema.load(data_post)  # Validate incoming data against the schema
        path = url_map[bleach.clean(result['path'])]  # Sanitize the validated path
        dtype = bleach.clean(result['type'])  # Sanitize the validated type
        question = bleach.clean(result['question'])  # Sanitize the validated question
        
        data = source.fit(
            path=path,
            dtype=dtype,
            chunk_size=1024
        )
        embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        retriever = retrieve.auto_retriever(
            data=data,
            embed_model=embed_model,
            type="normal",
            top_k=3
        )
        llm = GeminiModel(
            model_name="gemini-pro",
            google_api_key=GOOGLE_API_KEY
        )
        pipeline = generator.Generate(
            question=question,
            system_prompt="you are a smart AI chatbot, answer the question asked by the user",
            llm=llm,
            retriever=retriever
        )
        response = pipeline.call()
        return jsonify({"response": response})
    except ValidationError as err:
        logging.error(f"Validation error in /ai endpoint: {err}")  # Log validation errors
        return jsonify({"error": err.messages}), 400  # Return validation errors to the client
    except Exception as e:
        logging.error(f"Error in /ai endpoint: {e}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
