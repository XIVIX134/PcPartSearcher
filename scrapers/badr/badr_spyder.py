import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BadrSpyder:
    def __init__(self):
        """
        Initialize the BadrSpyder class.
        
        Args:
            save_html (bool): If True, save the fetched HTML content to a file for debugging.
        """
        self.base_url = "https://elbadrgroupeg.store/index.php?route=product/search&search="
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }

    async def scrap(self, search_term: str) -> str:
        """
        Search products on Badr asynchronously and return product details.

        Args:
            search_term (str): The search term to query on Badr.

        Returns:
            str: JSON string containing product details.
        """
        url = f"{self.base_url}{search_term}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                logger.info(f"[ ElBadr Spider ] Fetching El Badr Group data from URL: {url}")
                async with session.get(url) as response:
                    if response.status != 200:
                        logger.error(f"[ ElBadr Spider ] Failed to fetch data. HTTP Status Code: {response.status}")
                        return json.dumps({"error": f"Failed to fetch data. HTTP Status Code: {response.status}"})
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')


                    #   with open("badr_results.html", 'w', encoding='utf-8') as f:
                    #       f.write(html)

                    list_of_products = soup.find('div', class_='main-products main-products-style product-grid ipr-grid')

                    if not list_of_products:
                        return json.dumps({"error": "No products found on the page"})
                    
                    product_divs = list_of_products.find_all('div', class_='product-layout')
                    
                    logger.info(f"[ ElBadr Spider ] Found {len(product_divs)} products on the page")

                    products = []   

                    for div in product_divs:
                        try:
                            details = {}

                            # Product ID
                            details['product_id'] = div.get('data-product-id', "N/A")

                            # Product name
                            name_tag = div.select_one('.name a')
                            details['name'] = name_tag.text.strip() if name_tag else "N/A"

                            # Product URL
                            details['url'] = name_tag['href'] if name_tag and 'href' in name_tag.attrs else "N/A"

                            # Product image URL
                            img_tag = div.select_one('.product-img img')
                            details['image_url'] = img_tag['src'] if img_tag else "N/A"

                            # Description
                            description_tag = div.select_one('.description')
                            details['description'] = description_tag.text.strip() if description_tag else "N/A"

                            # Product price (new)
                            price_new_tag = div.select_one('.price .price-normal')
                            details['price_new'] = price_new_tag.text.strip() if price_new_tag else "N/A"

                            # Tax price
                            tax_price_tag = div.select_one('.price .price-tax')
                            details['tax_price'] = tax_price_tag.text.replace('Ex Tax:', '').strip() if tax_price_tag else "N/A"

                            # Brand
                            brand_tag = div.select_one('.stat-1 a')
                            details['brand'] = brand_tag.text.strip() if brand_tag else "N/A"

                            # Model
                            model_tag = div.select_one('.stat-2 span:nth-child(2)')
                            details['model'] = model_tag.text.strip() if model_tag else "N/A"

                            # Labels (e.g., New, Discount)
                            labels = div.select('.product-labels span')
                            details['labels'] = [label.text.strip() for label in labels] if labels else []

                            # Product rating (stars)
                            rating_stars = div.select('.rating-stars .fa-star')
                            details['rating'] = len(rating_stars)

                            products.append(details)
                        except Exception as e:
                            print(f"Error processing product div: {e}")
                            continue

                    return products
            except Exception as e:
                return e


# Example usage
# async def main():
#     spyder = BadrSpyder()
#     search_results = await spyder.scrap("hp")
#     with open("badr_results.json", 'w', encoding='utf-8') as f:
#         json.dump(search_results, f, indent=4)

#     print("Data successfully written to badr.json")

# asyncio.run(main())