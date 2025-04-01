import google.generativeai as genai
import re
import json
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  
genai.configure(api_key=GOOGLE_API_KEY)

def load_claims(file_path):
    """Load claims from the JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['claims']

def query_gemini_flash(claim):
    model = genai.GenerativeModel("gemini-1.5-flash") 
    prompt = f"""
    Evaluate the truthfulness of the following claim on a scale from 0 to 1, where:
    - 1.0 means the claim is completely true.
    - 0.0 means the claim is completely false.
    - Values in between indicate partial truth.

    Claim: "{claim}"

    Provide only the score as a number between 0 and 1.
    """
    response = model.generate_content(prompt)
    return response.text.strip() 

def extract_score(response_text):
    match = re.search(r'(\d*\.?\d+)', response_text) 
    if match:
        return float(match.group(1))  
    return None  

claims = load_claims('data/claims.json')  

for claim in claims:
    response_text = query_gemini_flash(claim)
    truthfulness_score = extract_score(response_text)

    rating = "Inconclusive" 
    if truthfulness_score is not None:
        if truthfulness_score == 1.0:
            rating = "True"
        elif truthfulness_score == 0.0:
            rating = "False"
        else:
            rating = "Partially True"  

    print(f"Score: {truthfulness_score if truthfulness_score is not None else 'Error'}")
