import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import logging
from typing import List, Optional, Dict, Any
import json
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.dubizzle.com.eg"
BATCH_SIZE = 10  # Increased number of concurrent requests

HEADERS = {
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

class OLX_Spyder:
    def __init__(self, search_term: str):
        self.search_term = search_term.replace(' ', '-')
        self.base_search_url = f"https://www.dubizzle.com.eg/en/electronics-home-appliances/computers-accessories/q-{self.search_term}"

    async def fetch_page(self, session: aiohttp.ClientSession, url: str, page: int) -> Optional[str]:
        """Fetches a single page"""
        try:
            async with session.get(url, headers=HEADERS) as response:
                if response.status == 404:
                    logger.info(f"Page {page} not found (404)")
                    return None

                if response.status != 200:
                    logger.error(f"Failed to fetch page {page}. Status: {response.status}")
                    return None

                html = await response.text()
                return html

        except Exception as e:
            logger.error(f"Error fetching page {page}: {str(e)}")
            return None

    def parse_page(self, html: str, page: int) -> List[Dict[str, Any]]:
        """Parses a single page"""
        soup = BeautifulSoup(html, 'html.parser')
        data_list = []
        listings = soup.find_all('li', attrs={'aria-label': 'Listing'})

        for listing in listings:
            title_tag = listing.find('h2', class_='_941ffa5e')
            price_tag = listing.find('span', class_='_1f2a2b47')
            location_tag = listing.find('span', class_='_77000f35')
            image_tag = listing.find('img', class_='f79152f1')
            link_tag = listing.find('a', href=True)

            if link_tag:
                details_link = BASE_URL + link_tag['href']
                match = re.search(r'-ID(\d+)', link_tag['href'])
                product_id = match.group(1) if match else "N/A"
            else:
                details_link = product_id = "N/A"

            data_list.append({
                "Product ID": product_id,
                "Title": title_tag.text.strip() if title_tag else "N/A",
                "Price": price_tag.text.strip() if price_tag else "N/A",
                "Tax": "0 EGP",
                "Location": location_tag.text.strip() if location_tag else "N/A",
                "Details Link": details_link,
                "Image URL": image_tag['src'] if image_tag else "N/A",
                "Stock": "Contact Owner", 
                "Brand": "N/A",
                "Model": "N/A",
                "Labels": ["Used", "No Warranty", "C2C"],
                "Rating": 5,
                "Description": title_tag.text.strip() if title_tag else "N/A",
                "Page": page
            })

        logger.info(f"Found {len(data_list)} listings on page {page}")
        return data_list

    async def scrape_olx_async(self) -> List[Dict[str, Any]]:
        """Scrapes all pages concurrently in batches"""
        if not self.search_term:
            return []

        async with aiohttp.ClientSession() as session:
            # First get page 1 to check if search has results
            first_page_html = await self.fetch_page(session, self.base_search_url, 1)
            if not first_page_html:
                return []

            all_html_pages = [first_page_html]
            current_page = 2

            while True:
                # Create batch of concurrent requests
                batch_tasks = []
                for i in range(BATCH_SIZE):
                    page_num = current_page + i
                    url = f"{self.base_search_url}/?page={page_num}"
                    batch_tasks.append(self.fetch_page(session, url, page_num))

                # Execute batch concurrently
                batch_results = await asyncio.gather(*batch_tasks)

                # Process results and check for end of pages
                found_404 = False
                new_html_pages = []

                for result in batch_results:
                    if result is None:  # 404 encountered
                        found_404 = True
                        break
                    if result:
                        new_html_pages.append(result)

                all_html_pages.extend(new_html_pages)

                if found_404 or not new_html_pages:
                    break

                current_page += BATCH_SIZE
                if current_page > 50:  # Increased safety limit
                    break

            # Parse all fetched pages
            all_results = []
            for page_num, html in enumerate(all_html_pages, start=1):
                all_results.extend(self.parse_page(html, page_num))

            return all_results

    async def scrape(self) -> List[Dict[str, Any]]:
        """Scrapes the listings asynchronously"""
        return await self.scrape_olx_async()

# Example Usage
async def main():
    spyder = OLX_Spyder("rtx")
    results = await spyder.scrape()
    with open('olx_products.json', 'w') as f:
      f.write(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())