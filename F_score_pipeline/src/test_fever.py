import json
from fever_model import get_fever_score, retrieve_top_evidence

def load_claims(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['claims'] 

claims = load_claims('data/claims.json') 

for claim in claims:
    top_evidence, scores = retrieve_top_evidence(claim) 
    fever_score = get_fever_score(claim, top_evidence) 

    print(f"Score: {fever_score}\n")
