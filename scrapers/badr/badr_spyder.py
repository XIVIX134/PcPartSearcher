import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

class BadrSpyder:
    def __init__(self):
        self.base_url = "https://elbadrgroupeg.store/index.php?route=product/search&search="
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

    async def search(self, search_term: str) -> str:
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
                async with session.get(url) as response:
                    if response.status != 200:
                        return json.dumps({"error": f"Failed to fetch data. HTTP Status Code: {response.status}"})
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    product_divs = soup.find_all('div', class_='product-layout')
                    products = []

                    for div in product_divs:
                        try:
                            details = {}

                            # Extract product name
                            name_tag = div.select_one('.name a')
                            details['name'] = name_tag.text.strip() if name_tag else "N/A"

                            # Extract product URL
                            details['url'] = name_tag['href'] if name_tag and 'href' in name_tag.attrs else "N/A"

                            # Extract product image URL
                            img_tag = div.select_one('.product-img img')
                            details['image_url'] = img_tag['src'] if img_tag else "N/A"

                            # Extract brand
                            brand_tag = div.select_one('.stat-1 a')
                            details['brand'] = brand_tag.text.strip() if brand_tag else "N/A"

                            # Extract model
                            model_tag = div.select_one('.stat-2 span:last-child')
                            details['model'] = model_tag.text.strip() if model_tag else "N/A"

                            # Extract description
                            desc_tag = div.select_one('.description')
                            details['description'] = desc_tag.text.strip() if desc_tag else "N/A"

                            # Extract price
                            price_tag = div.select_one('.price-normal')
                            details['price'] = price_tag.text.strip() if price_tag else "N/A"

                            # Extract tax price
                            tax_price_tag = div.select_one('.price-tax')
                            details['tax_price'] = tax_price_tag.text.replace('Ex Tax:', '').strip() if tax_price_tag else "N/A"

                            products.append(details)
                        except AttributeError:
                            continue

                    return json.dumps(products)
            except Exception as e:
                return json.dumps({"error": f"An exception occurred: {str(e)}"})

# Example usage
# async def main():
#     spyder = BadrSpyder()
#     search_results = await spyder.search("rtx")
#     parsed_results = json.loads(search_results)
#     
#     with open("badr.json", 'w', encoding='utf-8') as f:
#         json.dump(parsed_results, f, ensure_ascii=False, indent=4)
#     
#     print("Data successfully written to badr.json")

# asyncio.run(main())
