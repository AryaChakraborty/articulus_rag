<div align="center">
<h1 align="center">Articulus-RAG</h1>
<h2 align="center">Develop - Prototype - Assess - Iterate</h2>

<a href="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-3776AB.svg?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python Versions"></a>
<a href="https://twitter.com/ChakrabortyAry1"><img src="https://img.shields.io/twitter/follow/Arya" alt="Twitter" /></a>
<a href="https://twitter.com/sbk_2k1"><img src="https://img.shields.io/twitter/follow/Saptarshi" alt="Twitter" /></a>

<p>A platform for empowering transparency in media leverages AI-driven chatbots and content from journalism students to provide credible insights on global affairs, addressing gaps in Indian journalism. Inspired by my struggle to find concise information on India's stance on the Russia-Ukraine conflict during an interview preparation, and concerns about biased media coverage in regions like Manipur and Ladakh, the project aims to promote factual reporting and informed discourse. By offering accurate responses to complex queries and fostering a culture of fact-based reporting, it seeks to mitigate the prevalence of biased or incomplete information in Indian media, promoting transparency, accountability, and knowledge dissemination in the digital age.</p>

</div>

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
    "question": "What is the blog talking about?"
  }
  ```
- **Response:**
  - Success: Returns a JSON object containing the response from the enterprise RAG model.
  - Error: Returns a JSON object with an error message.

## Acknowledgements

* [HuggingFace](https://github.com/huggingface)
* [LlamaIndex](https://github.com/jerryjliu/llama_index)
* [Google Gemini](https://ai.google.dev/)
  
and the entire OpenSource community.
