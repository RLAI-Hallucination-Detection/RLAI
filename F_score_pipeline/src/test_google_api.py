import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

FACT_CHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
KG_API_URL = "https://kgsearch.googleapis.com/v1/entities:search"

FACT_CHECK_API_KEY = os.getenv("FACT_CHECK_API_KEY")  
KG_API_KEY = os.getenv("KG_API_KEY")  


def load_claims(file_path):
    """Load claims from the JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['claims'] 


def get_claims(query):
    """Fetch claim reviews from Google Fact Check API"""
    params = {'query': query, 'key': FACT_CHECK_API_KEY}
    response = requests.get(FACT_CHECK_API_URL, params=params)
    
    if response.status_code != 200:
        print("⚠ Fact Check API request failed.")
        return None

    data = response.json()
    claims = data.get('claims', [])

    if not claims:
        print("❌ No claims found in Fact Check API.")
        return None

    for claim in claims:
        claim_text = claim.get('text', "").lower()
        review_rating = claim.get('claimReview', [{}])[0].get('textualRating', "")

        if query.lower() in claim_text:
            if 'true' in review_rating.lower():
                return {"rating": "True", "score": 1.0}
            elif 'false' in review_rating.lower():
                return {"rating": "False", "score": 0.0}
            elif 'inconclusive' in review_rating.lower():
                return {"rating": "Inconclusive", "score": 0.5}

    return None


def get_knowledge_graph_info(query):
    """Fetch entity details from Google Knowledge Graph API"""
    params = {'query': query, 'key': KG_API_KEY, 'limit': 1, 'indent': True, 'languages': 'en'}
    response = requests.get(KG_API_URL, params=params)

    if response.status_code != 200:
        print("⚠ Knowledge Graph API request failed.")
        return None

    data = response.json()
    if 'itemListElement' in data and len(data['itemListElement']) > 0:
        entity = data['itemListElement'][0]['result']
        return {
            "name": entity.get('name', 'Unknown'),
            "description": entity.get('description', 'No description available'),
            "detailed_info": entity.get('detailedDescription', {}).get('articleBody', 'No details found'),
            "source": entity.get('detailedDescription', {}).get('url', 'No source found')
        }

    return None


def get_final_truth_score(query):
    """Combines Fact Check API and Knowledge Graph API for validation"""
    fact_check_result = get_claims(query)

    if fact_check_result:
        return fact_check_result
    
    kg_data = get_knowledge_graph_info(query)

    if kg_data:
        return {"score": 0.9}

    return {"score": 0.5}


claims = load_claims('data/claims.json') 

for claim in claims:
    result = get_final_truth_score(claim)
    print(f"Score: {result['score']}")

