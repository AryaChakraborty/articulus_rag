import requests
from bs4 import BeautifulSoup

def get_url_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Send a GET request to the URL with custom headers
        response = session.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text from the HTML content
        text = soup.get_text(separator='\n')
        
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL content: {e}")
        return None
