import requests
from bs4 import BeautifulSoup

def search_fact_database(claim):
    # Dummy implementation, replace with actual database/API calls
    query = "+".join(claim.split())
    url = f"https://www.factcheck.org/search/{query}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        results = [a.text for a in soup.find_all('a', href=True)]
        return {"claim": claim, "results": results[:5]}
    return {"claim": claim, "results": ["No results found"]}
