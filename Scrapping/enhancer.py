import os 
import requests
from google import genai

from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API")

class Enhancer:
    """Class to enhance search queries and content using Gemini AI."""

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key is missing! Add it to .env")

        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def enhance_query(self, original_query: str) -> str:

        prompt = f"""
        Optimize this search query for maximum relevant web search results:
        {original_query}
        Return ONLY ONE search query.
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt]
        )
        return response.text

    def enhance_content(self, original_content: str) -> str:

        prompt = f"""
        OPTIMIZE and SUMMARIZE this content for maximum relevance and clarity:

        {original_content}
        
        DO NOT miss out on any important information.
        DO NOT add any new information.
        DO NOT change the meaning of the content.
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt]
        )
        return response.text