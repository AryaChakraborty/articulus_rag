## Quick install

To install Articulus RAG i.e., a private repo, we can use the Access Token of GitHub. 

```bash
git clone https://<UPDATE-WITH-YOUR-TOKEN>@https://github.com/AryaChakraborty/articulus_rag
```

Create virtual environment

```bash
python3 -m venv env 
source env/bin/activate

or

virtualenv env
source env/bin/activate
```

Install all the packages within the virtual environment. 

```bash
pip install -r requirements.txt
```

Install the beyondllm framework. 

```bash
pip install -e .
```

### API Documentation

#### /recommend Endpoint
- **Method:** GET
- **Description:** Retrieves ranked documents from the MongoDB collection.
- **Parameters:** None
- **Response:**
  - Success: Returns a JSON object containing the ranked documents.
  - Error: Returns a JSON object with an error message.

#### /rank Endpoint
- **Method:** POST
- **Description:** Retrieves ranked documents based on search keywords.
- **Parameters:**
  - search_keywords: List of search keywords.
- **Request Body Example:**
  ```json
  {
    "search_keywords": ["keyword1", "keyword2", "keyword3"]
  }
  ```
- **Response:**
  - Success: Returns a JSON object containing the ranked documents.
  - Error: Returns a JSON object with an error message.

#### /keyword_extractor Endpoint
- **Method:** POST
- **Description:** Extracts top 10 keywords from the given text.
- **Parameters:**
  - text: Input text from which keywords need to be extracted.
- **Request Body Example:**
  ```json
  {
    "body": "Input text for keyword extraction."
  }
  ```
- **Response:**
  - Success: Returns a JSON object containing the extracted keywords.
  - Error: Returns a JSON object with an error message.

#### /ai Endpoint
- **Method:** POST
- **Description:** Uses the enterprise RAG model to provide a response to the given question.
- **Parameters:**
  - path: URL path or source of the content.
  - type: Type of content (e.g., "url", "youtube", etc.).
  - question: Question to be answered.
- **Request Body Example:**
  ```json
  {
    "path": "https://highonbugs.sbk2k1.in/sows",
    "type": "url",
    "question": "What is the blog about?"
  }
  ```
- **Response:**
  - Success: Returns a JSON object containing the response from the enterprise RAG model.
  - Error: Returns a JSON object with an error message.