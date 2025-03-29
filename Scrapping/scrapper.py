import os 
import re 

import requests
from bs4 import BeautifulSoup
from firecrawl import FirecrawlApp

from dotenv import load_dotenv 
load_dotenv()

FIRECRAWL_API = os.getenv("FIRECRAWL_API")

class WebScraper:
    def __init__(self):
        if not FIRECRAWL_API:
            raise ValueError("Firecrawl API key is missing! Add it to .env")

        self.app = FirecrawlApp(api_key=FIRECRAWL_API)
        self.output_dir = "Sessions"
        os.makedirs(self.output_dir, exist_ok=True)

    def clean_text(self, content: str) -> str:
        soup = BeautifulSoup(content, "html.parser")
        extracted_text = []

        for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            extracted_text.append(f"\n{heading.name.upper()}: {heading.get_text(strip=True)}")

        for paragraph in soup.find_all("p"):
            extracted_text.append(paragraph.get_text(strip=True))

        for li in soup.find_all("li"):
            extracted_text.append(f"• {li.get_text(strip=True)}")

        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                cells = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
                extracted_text.append(" | ".join(cells))

        return "\n".join(extracted_text) if extracted_text else "No relevant text found."

    def scrape(self, url: str) -> str:
        print(f"\n🔍 Scraping: {url}")

        scrape_result = self.app.scrape_url(url, params={'formats': ['html']})
        if 'html' not in scrape_result or not scrape_result['html']:
            print("❌ No HTML content found.")
            return [False,None]

        filtered_text = self.clean_text(scrape_result['html'])

        file_path = os.path.join(self.output_dir, "Cleaned.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(filtered_text)

        print(f"✅ Saved: {file_path}")
        return [True,filtered_text]

    def crawl(self, url: str, depth: int = 1, limit: int = 100) -> str:
        print(f"\n🔍 Crawling: {url} (Depth: {depth})")

        crawl_status = self.app.crawl_url(
            url,
            params={
                'limit': limit,
                'scrapeOptions': {'formats': ['html']}
            },
            poll_interval=30
        )

        if 'pages' not in crawl_status:
            print("❌ No pages found!")
            return [False,None]

        all_text = []

        for i, page in enumerate(crawl_status['pages']):
            page_url = page['url']
            print(f"📄 Scraping page {i+1}: {page_url}")

            page_data = self.app.scrape_url(page_url, params={'formats': ['html']})
            if 'html' in page_data and page_data['html']:
                filtered_text = self.clean_text(page_data['html'])
                all_text.append(filtered_text)

        merged_content = "\n\n".join(all_text)

        file_path = os.path.join(self.output_dir, "Cleaned.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(merged_content)

        print(f"✅ Saved: {file_path}")
        return [True, merged_content]