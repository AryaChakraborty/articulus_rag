from flask import Flask, request, jsonify
from flask_cors import CORS
from enterprise_rag import source,retrieve,embeddings,llms,generator
from utils import keyword_from_search_sentence
from dotenv import load_dotenv # type: ignore
load_dotenv()
import os

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend_endpoint():
    pass

@app.route('/rank', methods=['POST'])
def rank_endpoint():
    pass

@app.route('/keyword_extractor', methods=['POST'])
def yake_endpoint():
    '''
    takes data in the form of a dictionary with the key 'text' and returns the top 10 keywords from the text.
    '''
    data = request.json
    text = data.get('text')
    keywords = keyword_from_search_sentence(text)
    return jsonify({"keywords": keywords})

@app.route('/ai', methods=['POST'])
def ai_endpoint():
    data_post = request.json
    path = data_post.get('path') # https://highonbugs.sbk2k1.in/blog1
    dtype = data_post.get('type') # "url", "youtube", etc.
    question = data_post.get('question') # What is the best way to learn python?

    data = source.fit(path=path,
                      dtype=dtype,
                      chunk_size=1024,
                      chunk_overlap=0)

    embed_model = embeddings.HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    retriever = retrieve.auto_retriever(data,embed_model,type="normal",top_k=4)

    llm = llms.GeminiModel(model_name="gemini-pro",
                           google_api_key = os.getenv("GOOGLE_API_KEY"))

    pipeline = generator.Generate(question=question,
                                  retriever=retriever,
                                  llm=llm)
    
    response = pipeline.call()

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
