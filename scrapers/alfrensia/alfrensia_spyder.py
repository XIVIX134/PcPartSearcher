import requests
from bs4 import BeautifulSoup
import json


class ALFrensia_Spyder:
    def __init__(self):
        self.base_url = "https://alfrensia.com/en/?s={}&post_type=product"

    def scrap(self, search_term):
        search_term = search_term.replace(" ", "+")
        url = self.base_url.format(search_term)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch URL: {url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')


        col_large_9 = soup.find("div", class_="col large-9")
        print(f"Col large-9 found: {col_large_9}")
        if not col_large_9:
            print("Product container not found")
            return

        product_divs = col_large_9.find_all("div", class_="product-small col has-hover product type-product")
        print(f"Found product_divs with: {len(product_divs)} products")

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


if __name__ == "__main__":
    spyder = ALFrensia_Spyder()
    search_term = "rtx"
    results = spyder.scrap(search_term)
    
    output_file = f"alfrensia_{search_term.replace('+', '_')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
        print(f"Results saved to {output_file}")
