import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

class ALFrensia_Spyder:
    def __init__(self):
        self.base_url = "https://alfrensia.com/en/?s={}&post_type=product"
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

    async def scrap(self, search_term):
        """
        Scrape product information from ALFrensia asynchronously.

        Args:
            search_term (str): The search term to query.

        Returns:
            list: List of product dictionaries containing details like title, URL, image URL, and stock status.
        """
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

                    col_large_9 = soup.find("div", class_="col large-9")
                    if not col_large_9:
                        print("Product container not found")
                        return []

                    product_divs = col_large_9.find_all(
                        "div", class_="product-small col has-hover product type-product"
                    )
                    print(f"Found {len(product_divs)} products")

                    results = []
                    for product in product_divs:
                        try:
                            title = product.find("a", {"aria-label": True})["aria-label"]
                            product_url = product.find("a", {"aria-label": True})["href"]
                            image_url = product.find("img")["src"]
                            status = "Out of Stock" if "out-of-stock" in product.get("class", []) else "In Stock"

                            results.append({
                                "title": title,
                                "product_url": product_url,
                                "image_url": image_url,
                                "status": status,
                            })
                        except Exception as e:
                            print(f"Error parsing product: {e}")

                    return results
            except Exception as e:
                print(f"An error occurred: {e}")
                return []

# Example usage
async def main():
    spyder = ALFrensia_Spyder()
    search_term = "rtx"
    results = await spyder.scrap(search_term)

    output_file = f"alfrensia_{search_term.replace('+', '_')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
        print(f"Results saved to {output_file}")

# Run the asynchronous scraper
# asyncio.run(main())
