import json
from rank_bm25 import BM25Okapi
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_corpus(filepath):
    with open(filepath, 'r') as f:
        corpus = json.load(f)
    return corpus

def preprocess(text):
    return text.lower().split()

corpus = load_corpus('data/fever_corpus.json')
corpus_texts = [doc['text'] for doc in corpus] 

vectorizer = TfidfVectorizer()

corpus_tfidf = vectorizer.fit_transform(corpus_texts)

def retrieve_top_evidence(claim, top_n=1):
    claim_tfidf = vectorizer.transform([claim])
    
    cosine_similarities = cosine_similarity(claim_tfidf, corpus_tfidf).flatten()

    top_indices = cosine_similarities.argsort()[-top_n:][::-1]
    top_evidence = [corpus[i]['text'] for i in top_indices]
    top_scores = [cosine_similarities[i] for i in top_indices]
    return top_evidence, top_scores

def get_fever_score(claim, top_evidence):
    """
    Return a dynamic FEVER score based on the claim and the top evidence.
    The score is directly the cosine similarity between the claim and the evidence.
    """
    texts = [claim] + top_evidence
    
    tfidf_matrix = vectorizer.transform(texts)
    
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    return similarity_matrix[0][0] 
