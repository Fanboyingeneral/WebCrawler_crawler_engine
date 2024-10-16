from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

def get_crawl_delay(url):
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception as e:
        raise Exception(f"Error reading robots.txt: {e}")

    if rp.can_fetch("*", url):
        return rp.crawl_delay("*") or 1  # Default to 1 second
    else:
        raise Exception(f"Crawling forbidden for {url} by robots.txt")
