import requests
from bs4 import BeautifulSoup
import json

# headers={
#         "Host": "www.amazon.com",
#         "Connection": "keep-alive",
#         "Cache-Control": "max-age=0",
#         "device-memory": "8",
#         "sec-ch-device-memory": "8",
#         "dpr": "2",
#         "sec-ch-dpr": "2",
#         "viewport-width": "1920",
#         "sec-ch-viewport-width": "1920",
#         "rtt": "50",
#         "downlink": "10",
#         "ect": "4g",
#         "sec-ch-ua": 'Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
#         "sec-ch-ua-mobile": "?0",
#         "sec-ch-ua-platform": "macOS",
#         "Upgrade-Insecure-Requests": "1",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#         "Sec-Fetch-Site": "same-origin",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-User": "?1",
#         "Sec-Fetch-Dest": "document",
#         "Referer": "https://www.amazon.com/",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "en-US,en;q=0.8"
# }

class BadrSpyder:
    def __init__(self):
        self.base_url = "https://elbadrgroupeg.store/index.php?route=product/search&search="

    def search(self, search_term):
        """
        Search products on Badr and return product details.

        Args:
            search_term (str): The search term to query on Badr.

        Returns:
            str: JSON string containing product details.
        """
        url = f"{self.base_url}{search_term}"
        headers = {
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return json.dumps({"error": f"Failed to fetch data. HTTP Status Code: {response.status_code}"})

        soup = BeautifulSoup(response.text, 'html.parser')
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

# Example usage
if __name__ == '__main__':
    spyder = BadrSpyder()
    search_results = spyder.search("rtx")

    parsed_results = json.loads(search_results)

    with open("badr.json", 'w', encoding='utf-8') as f:
        json.dump(parsed_results, f, ensure_ascii=False, indent=4)

    print("Data successfully written to badr.json")