import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import logging
from typing import List, Optional, Dict, Any
from aiohttp import ClientTimeout

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.dubizzle.com.eg"
BATCH_SIZE = 5  # Number of concurrent requests

async def fetch_page(session: aiohttp.ClientSession, url: str, page: int) -> Optional[List[Dict[str, Any]]]:
    """Fetches and parses a single page"""
    try:
        async with session.get(url) as response:
            if response.status == 404:
                logger.info(f"Page {page} not found (404)")
                return None
            
            if response.status != 200:
                logger.error(f"Failed to fetch page {page}. Status: {response.status}")
                return []
            
            html = await response.text()
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
                    "Location": location_tag.text.strip() if location_tag else "N/A",
                    "Image URL": image_tag['src'] if image_tag else "N/A",
                    "Details Link": details_link,
                    "Page": page
                })
            
            logger.info(f"Found {len(data_list)} listings on page {page}")
            return data_list
            
    except Exception as e:
        logger.error(f"Error fetching page {page}: {str(e)}")
        return []

async def scrape_olx_async(search_term: str) -> List[Dict[str, Any]]:
    """Scrapes all pages concurrently in batches"""
    if not search_term:
        return []

    processed_term = search_term.replace(' ', '-')
    base_search_url = f"https://www.dubizzle.com.eg/en/electronics-home-appliances/computers-accessories/q-{processed_term}"
    
    timeout = ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # First get page 1 to check if search has results
        first_page = await fetch_page(session, base_search_url, 1)
        if not first_page:
            return []
        
        all_results = first_page
        current_page = 2
        
        while True:
            # Create batch of concurrent requests
            batch_tasks = []
            for i in range(BATCH_SIZE):
                page_num = current_page + i
                url = f"{base_search_url}/?page={page_num}"
                batch_tasks.append(fetch_page(session, url, page_num))
            
            # Execute batch concurrently
            batch_results = await asyncio.gather(*batch_tasks)
            
            # Process results and check for end of pages
            found_404 = False
            new_results = []
            
            for result in batch_results:
                if result is None:  # 404 encountered
                    found_404 = True
                    break
                if result:
                    new_results.extend(result)
            
            all_results.extend(new_results)
            
            if found_404 or not new_results:
                break
                
            current_page += BATCH_SIZE
            if current_page > 20:  # Safety limit
                break
        
        return all_results

def scrape_olx(search_term: str, page: int = 1) -> List[Dict[str, Any]]:
    """Synchronous wrapper for async scraping"""
    results = asyncio.run(scrape_olx_async(search_term))
    
    # Sort results by page
    results.sort(key=lambda x: x.get('Page', 1))
    if page > 1:
        return [r for r in results if r.get('Page') == page]
    return results