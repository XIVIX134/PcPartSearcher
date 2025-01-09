import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, unquote

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
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"Failed to fetch URL: {url}")
                        return []

                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    product_container = soup.find("div", class_="col large-9")
                    if not product_container:
                        print("No product container found.")
                        return []

                    products = []
                    product_cards = product_container.find_all("div", class_="product-small")

                    for card in product_cards:
                        title_elem = card.find("a", class_="woocommerce-LoopProduct-link")
                        url = title_elem["href"] if title_elem and "href" in title_elem.attrs else "No URL"
                        title = title_elem.get("title", "").strip() if title_elem else self.extract_title_from_url(url)
                        
                        image_elem = card.find("img")
                        image_url = image_elem["src"] if image_elem else "No Image URL"

                        stock_status = "In Stock" if "instock" in card["class"] else "Out of Stock"
                        
                        
                        price_elem = card.find("span", class_="woocommerce-Price-amount amount")
                        price = price_elem.get_text(strip=True) if price_elem else "No Price"

                        products.append({
                            "title": title,
                            "url": url,
                            "image_url": image_url,
                            "price": price,
                            "stock_status": stock_status,
                        })

                    return products

            except Exception as e:
                print(f"An error occurred: {e}")
                return []


# async def main():
#     spider = ALFrensia_Spyder()
#     search_term = "rtx"
#     products = await spider.scrap(search_term)
#     with open('alfrensia_products.json', 'w') as f:
#         f.write(json.dumps(products, indent=2))


# asyncio.run(main())
