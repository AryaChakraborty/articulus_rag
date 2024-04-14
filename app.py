import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from enterprise_rag import source,retrieve,embeddings,llms,generator
from utils.keywordExtractor import keyword_from_search_sentence
from utils.rankBlogs import rank_documents
from dotenv import load_dotenv # type: ignore
import pymongo as pym
load_dotenv()
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
        # displaying all documents while sorting based on the search keywords.
        ranked_documents = rank_documents(search_keywords=search_keywords,
                                          documents=documents,
                                          users=users, 
                                          search_filter=False)
        ranked_list = [{'title': doc[0], 'user': doc[1], 'slug': doc[2]} for doc in ranked_documents]
        return jsonify({"ranked_documents": ranked_list})
    except Exception as e:
        logging.error(f"Error in /recommend endpoint: {e}")
        return jsonify({"error": str(e)})

@app.route('/rank', methods=['POST'])
def rank_endpoint():
    '''
    calls the rank_documents function with the search keywords from the data and the documents and returns the ranked documents.
    '''
    try:
        data = request.json
        documents = list(blog_collection.find({}))
        users = list(user_collection.find({}))
        search_keywords = data.get('search_keywords')
        # displaying all documents while sorting based on the search keywords.
        ranked_documents = rank_documents(search_keywords=search_keywords,
                                          documents=documents,
                                          users=users, 
                                          search_filter=True)
        ranked_list = [{'title': doc[0], 'user': doc[1], 'slug': doc[2]} for doc in ranked_documents]
        return jsonify({"ranked_documents": ranked_list})
    except Exception as e:
        logging.error(f"Error in /rank endpoint: {e}")
        return jsonify({"error": str(e)})

@app.route('/keyword_extractor', methods=['POST'])
def yake_endpoint():
    '''
    takes data in the form of a dictionary with the key 'text' and returns the top 10 keywords from the text.
    '''
    try:
        data = request.json
        text = data.get('body')
        keywords = keyword_from_search_sentence(text)
        return jsonify({"keywords": keywords})
    except Exception as e:
        logging.error(f"Error in /keyword_extractor endpoint: {e}")
        return jsonify({"error": str(e)})

@app.route('/ai', methods=['POST'])
def ai_endpoint():
    '''
    takes data in the form of a dictionary with the keys 'path', 'type', and 'question' and returns the response from the enterprise RAG model.
    '''
    try:
        data_post = request.json
        path = data_post.get('path') # https://highonbugs.sbk2k1.in/sows
        dtype = data_post.get('type') # "url", "youtube", etc.
        question = data_post.get('question') # What is the best way to learn python?

        data = source.fit(path=path,
                        dtype=dtype,
                        chunk_size=1024,
                        chunk_overlap=0)

        embed_model = embeddings.HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        retriever = retrieve.auto_retriever(data,embed_model,type="normal",top_k=4)

        llm = llms.GeminiModel(model_name="gemini-pro",
                            google_api_key = GOOGLE_API_KEY)

        pipeline = generator.Generate(question=question,
                                    retriever=retriever,
                                    llm=llm)
        
        response = pipeline.call()

        return jsonify({"response": response})
    
    except Exception as e:
        logging.error(f"Error in /ai endpoint: {e}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
