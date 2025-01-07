import requests
from bs4 import BeautifulSoup
import re

class SigmaSpyder:
    def __init__(self, search_term):
        self.search_term = search_term
        self.base_url = "https://www.sigma-computer.com/search"
        self.params = {
            "search": search_term,
            "submit_search": "",
            "route": "product/search"
        }

    @staticmethod
    def sanitize_filename(search_term):
        return re.sub(r'[^\w\-]', '_', search_term)

    def fetch_data(self):
        response = requests.get(self.base_url, params=self.params)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            return None
        return response.content

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
                "title": title,
                "link": f"https://www.sigma-computer.com/{link}",
                "image": f"https://www.sigma-computer.com/{image}",
                "price_new": price_new,
                "price_old": price_old,
                "stock": stock_status,
                "description": description
            }
        except Exception as e:
            print(f"Error parsing product: {e}")
            return None

    def scrape(self):
        content = self.fetch_data()
        if not content:
            return None
        
        soup = BeautifulSoup(content, "html.parser")
        product_blocks = soup.find_all("div", class_="product-layout")
        
        results = []
        for product in product_blocks:
            product_data = self.parse_product(product)
            if product_data:
                results.append(product_data)
        
        return results

# Example usage:
# spyder = SigmaSpyder("laptop")
# results = spyder.scrape()
# print(results)