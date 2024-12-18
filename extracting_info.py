import vertexai
from vertexai.generative_models import GenerativeModel
import requests
from bs4 import BeautifulSoup

def extract_info_from_search_results(answer, n=1):
  
  #search_results = search_engine_api(search_query, n)

    extracted_data = ""
    
    count=0
    for result in answer:
        if (count>=n):
            break
        count+=count
        try:
            url = result.uri
            data = extract_info(url)
            extracted_data+=data
        except Exception as e:
            print(f"Error extracting information from {url}: {e}")

    return extracted_data

def extract_info(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_sections = soup.find_all('div', {'data-identity': 'article-section'})

    extracted_data = ""
    for section in article_sections:
        # Extract text from the section (adjust as needed)
        text = section.get_text(strip=True)
        extracted_data+=text
    

    return extracted_data