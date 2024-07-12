import spacy
from utils import search_fact_database

nlp = spacy.load('en_core_web_sm')

def check_fact(text):
    doc = nlp(text)
    claims = [sent.text for sent in doc.sents]
    results = []
    for claim in claims:
        result = search_fact_database(claim)
        results.append(result)
    return {"claims": claims, "results": results}
