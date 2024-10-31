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
    respect_robot_flag = data.get('respectRobotFlag')

    print("**********Crawler received Respect Robot Flag: ",respect_robot_flag)
    try:
        result,external_urls,message = await crawler.run_crawler(url, max_urls, respect_robot_flag)  

        #print(f"&&&&External URLs: {external_urls}")

        return {"message": message, "scraped_urls": result, "external_urls": external_urls}
    except Exception as e:
        return {"error": str(e)}
