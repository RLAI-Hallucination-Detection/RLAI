import json
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize

def load_claims(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['claims'] 

with open("data/fever_corpus.json", "r") as file:
    fever_corpus = json.load(file)

corpus_texts = [item["text"] for item in fever_corpus]
tokenized_corpus = [word_tokenize(doc.lower()) for doc in corpus_texts]
bm25 = BM25Okapi(tokenized_corpus)

def retrieve_top_evidence(claim, top_n=3):
    """Retrieve top evidence using BM25."""
    tokenized_claim = word_tokenize(claim.lower())
    scores = bm25.get_scores(tokenized_claim)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
    top_evidence = [corpus_texts[i] for i in top_indices]
    return top_evidence
