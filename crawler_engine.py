import asyncio
from collections import deque
from pymongo import MongoClient
from urllib.parse import urljoin, urlparse
from crawl4ai import WebCrawler
from utils.robot_utils import get_crawl_delay
from utils.file_utils import save_to_file, sanitize_filename
from utils.mongo_utils import save_to_mongodb

class WebCrawlerEngine:
    def __init__(self):
        self.data_storage = {}
        self.visited_urls = set()
        self.url_queue = deque()
        self.external_urls = set()
        self.crawler = WebCrawler()
        self.crawler.warmup()

    async def crawl_url(self, url):
        try:
            delay = get_crawl_delay(url)
            await asyncio.sleep(delay)

            result = self.crawler.run(url=url)
            print(f"Crawled URL: {url}")

            self.data_storage[url] = result.html

            base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

            if result.links and 'internal' in result.links:
                for link_data in result.links['internal']:
                    full_url = urljoin(base_url, link_data['href'])
                    if full_url not in self.visited_urls:
                        print(f"Adding internal URL to queue: {full_url}")
                        self.url_queue.append(full_url)

            if result.links and 'external' in result.links:
                for link_data in result.links['external']:
                    href = link_data['href']
                    if href not in self.visited_urls:
                        print(f"Discovered external URL: {href}")
                        self.external_urls.add(href)

            self.visited_urls.add(url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    async def run_crawler(self, seed_url, max_urls):
        self.url_queue.append(seed_url)

        while self.url_queue and len(self.visited_urls) < max_urls:
            current_url = self.url_queue.popleft()
            if current_url not in self.visited_urls:
                await self.crawl_url(current_url)

        save_to_mongodb(self.data_storage)

        return self.data_storage

