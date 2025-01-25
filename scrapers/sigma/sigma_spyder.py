import asyncio
import json
import aiohttp
from bs4 import BeautifulSoup
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SigmaSpyder")

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

class SigmaSpyder:
    def __init__(self, search_term):
        self.search_term = search_term
        self.base_url = "https://www.sigma-computer.com/search"
        self.params = {
            "search": search_term,
            "submit_search": "",
            "route": "product/search"
        }
        logger.info(f"Searching for: {search_term} in Sigma Computer")

    @staticmethod
    def sanitize_filename(search_term):
        return re.sub(r'[^\w\-]', '_', search_term)

    async def fetch_data(self, session):
        async with session.get(self.base_url, params=self.params) as response:
            content = await response.text()
            return content

    def parse_product(self, product):
        try:
            title = product.find("h4").text.strip()
            link = product.find("h4").find("a")["href"]
            image = product.find("img", class_="img-1")["src"]
            price_new = product.find("span", class_="price-new").text.strip()
            price_old = product.find("span", class_="price-old").text.strip() if product.find("span", class_="price-old") else None
            
            description_elements = product.find("div", class_="description").find_all("div")
            description = "\n".join([desc.text.strip() for desc in description_elements if desc.text.strip()])
            
            stock_status = "Unknown"
            stock_element = product.find("span", class_="stock")
            if stock_element:
                status_text = stock_element.text.strip().lower()
                if "متوفر" in status_text or "in stock" in status_text:
                    stock_status = "In Stock"
                elif "غير متوفر" in status_text or "out of stock" in status_text:
                    stock_status = "Out of Stock"
                else:
                    stock_span = product.find("span", class_="stock_Y") or product.find("span", class_="stock_N")
                    if stock_span:
                        if "stock_Y" in stock_span.get("class", []):
                            stock_status = "In Stock"
                        elif "stock_N" in stock_span.get("class", []):
                            stock_status = "Out of Stock"
            
            return {
                "Product ID": "", # TODO: Extract product ID from link
                "Title": title,
                "Price": price_new,
                "Tax": "0 EGP",
                "Location": "Sigma Computer",
                "Details Link": f"https://www.sigma-computer.com/{link}",
                "Image URL": f"https://www.sigma-computer.com/{image}",
                # "price_old": price_old,
                "Stock": stock_status,
                "Brand": "",    # TODO: Extract brand from description
                "Model": "",    # TODO: Extract model from description
                "Labels": ["New", "Warranty", "B2C"],
                "Rating": 5,
                "Description": description,
                "Page": 1
            }
        except Exception as e:
            logger.error(f"Error parsing product: {str(e)}")
            return None

    async def scrap(self):
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            content = await self.fetch_data(session)
            if not content:
                return None
            
            soup = BeautifulSoup(content, "html.parser")
            product_blocks = soup.find_all("div", class_="product-layout")
            
            results = []
            for product in product_blocks:
                product_data = self.parse_product(product)
                if product_data:
                    results.append(product_data)
        logger.info(f"Found {len(results)} products in Sigma Computer")
        
        return results


if __name__ == "__main__":
    search_term = "rtx"
    spyder = SigmaSpyder(search_term)
    results = asyncio.run(spyder.scrap())
    with open("sigma_results.json", "w") as f:
        f.write(json.dumps(results, indent=2))
