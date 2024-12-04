from flask import Flask, request, jsonify
from fact_check import check_fact

app = Flask(__name__)

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    result = check_fact(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)