import requests
from bs4 import BeautifulSoup
from flask import jsonify
import json 
class AmazonSpyder:
    def __init__(self):
        pass

    def search_products(self, search_term):
        """
        Search products on Amazon and return product details.

        Args:
            search_term (str): The search term to query on Amazon.

        Returns:
            str: JSON string containing product details.
        """
        # url = "https://www.amazon.eg/s?k={search_term}&crid=25ZTFGDJ21GUD&sprefix=hp%2Caps%2C197&ref=nb_sb_noss_1"
        url = f"https://www.amazon.eg/s?k={search_term}"
        headers = {
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        }

        
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return f"Failed to fetch data. HTTP Status Code: {response.status_code}"


        soup = BeautifulSoup(response.content, "html.parser")
        product_cards = soup.find_all("div", {"data-component-type": "s-search-result"})
        products = []

        for card in product_cards:
            try:
                title = card.find("h2").text.strip() if card.find("h2") else "N/A"

                link_div = card.find("div", class_="a-section a-spacing-none a-spacing-top-small s-title-instructions-style")
                
                if link_div and link_div.a:
                    link = "https://www.amazon.eg" + link_div.a["href"]
                    
                link = link if link else "N/A"
               
                price = card.find("span", class_="a-price-whole")
                price = price.text.strip() if price else "N/A"

                
                rating = card.find("span", class_="a-icon-alt")
                rating = rating.text.strip() if rating else "N/A"

                
                image_div = card.find("div", class_="a-section aok-relative s-image-square-aspect")
                image = image_div.img["src"] if image_div and image_div.img else "N/A"

                
                products.append({
                    "title": title,
                    "link": link,
                    "price": price,
                    "rating": rating,
                    "image": image
                })
            except AttributeError:
                continue


        return products

# Example usage
if __name__ == "__main__":
    scraper = AmazonSpyder()
    search_results = scraper.search_products("macbook")
    with open("amazon.json", "w", encoding='utf-8') as file:
        file.write(json.dumps(search_results, ensure_ascii=False, indent=4))
    
