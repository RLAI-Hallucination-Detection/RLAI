import os 
import requests

from dotenv import load_dotenv
load_dotenv()
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def websearch_url(enhanced_query, num_results=3): #Returns a list of URLs using Google Search API!

    search_url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        "q": enhanced_query,  
        "key": GOOGLE_SEARCH_API_KEY,  
        "cx": SEARCH_ENGINE_ID,  
        "num": num_results
    }
    
    response = requests.get(search_url, params=params)
    results = response.json()

    if "items" in results:
        return [item["link"] for item in results["items"]]
    else:
        return ["No results found"]