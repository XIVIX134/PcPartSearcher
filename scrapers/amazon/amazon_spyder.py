import asyncio
import json
import random
import logging
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AmazonSpyder")

# Number of concurrent requests
CONCURRENT_REQUESTS = 10

# User-Agent pool to randomize headers to avoid detection (untested in production) :(
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
]

class AmazonSpyder:
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        self.semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)  # Limit concurrency

    async def fetch_page(self, client: httpx.AsyncClient, search_term: str, page: int) -> Optional[List[Dict[str, Any]]]:
        """Fetch a single page and parse results."""
        async with self.semaphore:
            url = f"https://www.amazon.eg/s?k={search_term}&language=en&page={page}"
            self.headers["User-Agent"] = random.choice(USER_AGENTS)  # Rotate User-Agent, untested in production yet :(
            
            try:
                response = await client.get(url, headers=self.headers)
                if response.status_code == 404:
                    logger.info(f"Page {page} not found (404).")
                    return None

                if response.status_code != 200:
                    logger.error(f"Failed to fetch page {page}. Status: {response.status_code}")
                    return []

                html = response.text
                soup = BeautifulSoup(html, "html.parser")

                # Parse product data
                product_cards = soup.select("div[data-component-type='s-search-result']")
                products = []
                for card in product_cards:
                    try:
                        title = card.find("h2").text.strip() if card.find("h2") else "N/A"
                        link = f"https://www.amazon.eg{card.find('a')['href']}" if card.find("a") else None
                        price = card.select_one(".a-price-whole").text.strip() if card.select_one(".a-price-whole") else "N/A"
                        rating = card.select_one(".a-icon-alt").text.strip() if card.select_one(".a-icon-alt") else "N/A"
                        image = card.select_one("img")["src"] if card.select_one("img") else "N/A"

                        products.append({
                            "Title": title,
                            "Price": price,
                            "Rating": rating,
                            "Details Link": link,
                            "Image URL": image,
                            "Page": page,
                        })
                    except Exception:
                        continue

                logger.info(f"Found {len(products)} products on page {page}.")
                return products

            except Exception as e:
                logger.error(f"Error fetching page {page}: {str(e)}")
                return []

    async def scrap(self, search_term: str) -> List[Dict[str, Any]]:
        """Scrape products concurrently."""
        timeout = httpx.Timeout(30.0, connect=10.0)
        limits = httpx.Limits(max_connections=CONCURRENT_REQUESTS, max_keepalive_connections=20)

        async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
            tasks = [self.fetch_page(client, search_term, page) for page in range(1, 21)]
            all_results = await asyncio.gather(*tasks)

        # Flatten and filter results
        products = [product for result in all_results if result for product in result]
        return products


# Example usage
if __name__ == "__main__":
    spyder = AmazonSpyder()
    results = asyncio.run(spyder.scrap("rtx"))
    with open("amazon_results.json", "w") as f:
        f.write(json.dumps(results, indent=2))
