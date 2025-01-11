import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BATCH_SIZE = 5  # Number of concurrent requests

class AmazonSpyder:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }

    async def fetch_page(self, session: aiohttp.ClientSession, search_term: str, page: int) -> Optional[List[Dict[str, Any]]]:
        """Fetches and parses a single page"""
        try:
            url = f"https://www.amazon.eg/s?k={search_term}&language=en&page={page}"
            logger.info(f"[ Amazon.eg Spider ] Requesting page {page} with term {search_term} from URL: {url}")
            async with session.get(url, headers=self.headers) as response:
                if response.status == 404:
                    logger.info(f"[ Amazon.eg Spider ] Page {page} not found (404)")
                    return None
                
                if response.status != 200:
                    logger.error(f"[ Amazon.eg Spider ] Failed to fetch page {page}. Status: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                product_cards = soup.find_all("div", {"data-component-type": "s-search-result"})
                products = []

                for card in product_cards:
                    try:
                        title = card.find("h2").text.strip() if card.find("h2") else "N/A"
                        
                        link_div = card.find("div", class_="a-section a-spacing-none a-spacing-top-small s-title-instructions-style")
                        link = f"https://www.amazon.eg{link_div.a['href']}" if link_div and link_div.a else None
                        
                        price = card.find("span", class_="a-price-whole")
                        price = price.text.strip() if price else "N/A"
                        
                        rating = card.find("span", class_="a-icon-alt")
                        rating = rating.text.strip() if rating else "N/A"
                        
                        image_div = card.find("div", class_="a-section aok-relative s-image-square-aspect")
                        image = image_div.img["src"] if image_div and image_div.img else "N/A"

                        products.append({
                            "Product ID": "",
                            "Title": title,
                            "Price": price,
                            "Tax": "0 EGP",
                            "Location": "Amazon Egypt",
                            "Details Link": link,
                            "Image URL": image,
                            "Stock": "In Stock",
                            "Brand": "", # TODO: Extract brand
                            "Model": "", # TODO: Extract model
                            "Labels": ["NEW", "Warranty", "Delivery" "B2C"],
                            "Rating": rating,
                            "Description": "", # TODO: Extract description
                            "Page": page
                        })
                    except AttributeError:
                        continue

                logger.info(f"[ Amazon.eg Spider ] Found {len(products)} listings on page {page}")
                return products
                
        except Exception as e:
            logger.error(f"[ Amazon.eg Spider ] Error fetching page {page}: {str(e)}")
            return []

    async def search_products_async(self, search_term: str) -> List[Dict[str, Any]]:
        """Scrapes all pages concurrently in batches"""
        if not search_term:
            return []

        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            first_page = await self.fetch_page(session, search_term, 1)
            if not first_page:
                return []
            
            all_results = first_page
            current_page = 2
            
            while True:
                batch_tasks = []
                for i in range(BATCH_SIZE):
                    page_num = current_page + i
                    batch_tasks.append(self.fetch_page(session, search_term, page_num))
                
                batch_results = await asyncio.gather(*batch_tasks)
                
                found_404 = False
                new_results = []
                
                for result in batch_results:
                    if result is None:
                        found_404 = True
                        break
                    if result:
                        new_results.extend(result)
                
                all_results.extend(new_results)
                
                if found_404 or not new_results:
                    break
                    
                current_page += BATCH_SIZE
                if current_page > 20:
                    break
            
            return all_results

    def scrap(self, search_term: str, page: int = 1) -> List[Dict[str, Any]]:
        """Synchronous wrapper for async scraping"""
        results = asyncio.get_event_loop().run_until_complete(self.search_products_async(search_term))
        
        # Sort results by page
        results.sort(key=lambda x: x.get('Page', 1))
        if page > 1:
            return [r for r in results if r.get('Page') == page]
        return results
    
# Example usage:
# async def main():
#     amazon_spyder = AmazonSpyder()
#     results = await amazon_spyder.search_products_async("rtx")
#     with open('amazon_results.json', 'w') as f:
#         f.write(json.dumps(results, indent=2))
#
# if __name__ == '__main__':
#     asyncio.run(main())

