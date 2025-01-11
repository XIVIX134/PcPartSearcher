import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, unquote
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ALFrensia_Spyder:
    def __init__(self):
        self.base_url = "https://alfrensia.com/en/?s={}&post_type=product"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }
    
    def extract_title_from_url(self, url):
        try:
            path = urlparse(url).path
            slug = path.strip("/").split("/")[-1]
            slug = unquote(slug)
            title = slug.replace("-", " ").title()
            return title
        except Exception as e:
            print(f"Error parsing title from URL: {e}")
            return "No Title"

    async def scrap(self, search_term):
        search_term = search_term.replace(" ", "+")
        url = self.base_url.format(search_term)

        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                logger.info(f"[ ALFrensia Spider ] Fetching ALFrensia data from URL: {url}")
                async with session.get(url) as response:
                    if response.status != 200:
                        logger.error(f"[ ALFrensia Spider ] Failed to fetch data from {url}. HTTP Status Code: {response.status}")
                        return []

                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    product_container = soup.find("div", class_="col large-9")
                    if not product_container:
                        logger.error("No products found.")
                        return []

                    products = []
                    product_cards = product_container.find_all("div", class_="product-small")
                    
                    logger.info(f"[ ALFrensia Spider ] Found {len(product_cards)} products")

                    for card in product_cards:
                        title_elem = card.find("a", class_="woocommerce-LoopProduct-link")
                        url = title_elem["href"] if title_elem and "href" in title_elem.attrs else "No URL"
                        title = self.extract_title_from_url(url)
                        
                        image_elem = card.find("img")
                        image_url = image_elem["src"] if image_elem else "No Image URL"

                        stock_status = "In Stock" if "instock" in card["class"] else "Out of Stock"
                        
                        
                        price_elem = card.find("span", class_="woocommerce-Price-amount amount")
                        price = price_elem.get_text(strip=True) if price_elem else "No Price"

                        products.append({
                            "Product ID": "", # TODO: Extact product ID
                            "Title": title,
                            "Price": price,
                            "Tax": "0 EGP",
                            "Location": "Alfrensia Store",
                            "Details Link": url,
                            "Image URL": image_url,
                            "Stock": "In Stock", 
                            "Brand": "", # TODO: Extact product Brand
                            "Model": "", # TODO: Extact product Model
                            "Labels": ["NEW", "Warranty", "B2C"],
                            "Rating": 5,
                            "Description": "", # TODO: Extact product Description
                            "Page": 1
                        })

                    return products

            except Exception as e:
                print(f"An error occurred: {e}")
                return []


# async def main():
#     spider = ALFrensia_Spyder()
#     search_term = "rtx"
#     products = await spider.scrap(search_term)
#     with open('alfrensia_results.json', 'w') as f:
#         f.write(json.dumps(products, indent=2))


# asyncio.run(main())
