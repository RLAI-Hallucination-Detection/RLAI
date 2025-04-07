from google import genai
from bleurt import score as bleurt_score
from sentence_transformers import CrossEncoder

class HALMetrics:
    def __init__(self, gemini_api_key):
        # Init BLEURT scorer
        self.bleurt_scorer = bleurt_score.BleurtScorer("bleurt/bleurt-20")

        # Init CrossEncoder model
        self.crossencoder = CrossEncoder("cross-encoder/stsb-roberta-large")

        # Init Gemini client
        self.client = genai.Client(api_key="HAL_API_KEY")
    
    def BLEURT(self, query, llm_response, ground_truth):

        raw_score = self.bleurt_scorer.score(
            references=[ground_truth],
            candidates=[llm_response]
        )[0]

        normalized = min(max(raw_score, 0), 1)
        return round(normalized, 4)
    
    def CROSSENCODER(self, query, llm_response, ground_truth):

        raw_score = self.crossencoder.predict([(ground_truth, llm_response)])[0]
        normalized = min(max(raw_score / 5.0, 0), 1)

        return round(normalized, 4)

    def LLM_EVAL(self, query, llm_response, ground_truth):

        prompt = f"""
            You are a factual evaluator.
            Compare the following LLM response with the ground truth and score how factually correct it is on a scale of 0 (completely hallucinated) to 1 (fully grounded in the reference).
            Be strict. Focus on whether the meaning and facts match. Just paraphrasing is acceptable, but adding wrong or unrelated information is not.

            QUERY: {query}
            LLM RESPONSE: {llm_response}
            GROUND TRUTH: {ground_truth}

            Give only a number between 0 and 1. No explanation.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt]
            )
            score = int(response.text)
            normalized = min(max(score, 0), 1)

            return round(normalized, 4)

        except:
            return None
        
    def ALLSCORES(self, query, llm_response, ground_truth):

        s1 = self.BLEURT(query, llm_response, ground_truth)
        s2 = self.CROSSENCODER(query, llm_response, ground_truth)
        s3 = self.LLM_EVAL(query, llm_response, ground_truth)

        return [s1, s2, s3]