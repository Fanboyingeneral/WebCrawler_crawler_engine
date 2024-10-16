# main.py

from fastapi import FastAPI, Request
from crawler_engine import WebCrawlerEngine
import asyncio

app = FastAPI()
crawler = WebCrawlerEngine()  # Instantiate the engine

@app.post("/crawl")
async def crawl(request: Request):
    data = await request.json()
    url = data.get('url')
    max_urls = data.get('maxUrls')

    try:
        result = await crawler.run_crawler(url, max_urls)  # Call the method on the instance
        return {"message": "Crawl completed", "data": result}
    except Exception as e:
        return {"error": str(e)}
