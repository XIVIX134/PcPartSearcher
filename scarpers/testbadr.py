import requests
from bs4 import BeautifulSoup
import json

# Base URL for the site (correct URL structure)
BASE_URL = "https://elbadrgroupeg.store"
PRODUCT_LIST_URL = "https://elbadrgroupeg.store/cpu"

def get_product_details(product_url):
    """Scrapes individual product details."""
    response = requests.get(product_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product title
        title_tag = soup.find('h1', class_='product-title')
        title = title_tag.text.strip() if title_tag else "N/A"

        # Extract product description
        description_tag = soup.find('div', class_='description')
        description = description_tag.text.strip() if description_tag else "N/A"

        # Extract price
        price_tag = soup.find('span', class_='price-normal')
        price = price_tag.text.strip() if price_tag else "N/A"

        # Extract image URL
        image_tag = soup.find('img', class_='img-responsive')
        image_url = image_tag['src'] if image_tag else "N/A"

        # Extract product ID (from the product thumb div or hidden input)
        product_id_tag = soup.find('input', {'name': 'product_id'})
        product_id = product_id_tag['value'] if product_id_tag else "N/A"

        return {
            'Product ID': product_id,
            'Title': title,
            'Description': description,
            'Price': price,
            'Image URL': image_url,
            'Details Link': product_url
        }
    return {}

def scrape_first_page():
    """Scrapes only the first page of products."""
    url = PRODUCT_LIST_URL
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all products
        products = soup.find_all('div', class_='product-layout')

        product_data = []
        for product in products:
            # Ensure the full product URL is formed correctly
            product_url = product.find('a', class_='product-img')['href']
            product_url = BASE_URL + product_url if not product_url.startswith('http') else product_url

            product_details = get_product_details(product_url)
            if product_details:
                product_data.append(product_details)
        
        return product_data
    return []

def main():
    print("Scraping the first page of products...")
    products = scrape_first_page()
    
    if products:
        # Save to a JSON file
        with open('badr.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
        print(f"Scraped {len(products)} products and saved to 'products_first_page.json'")
    else:
        print("No products found on the first page.")

if __name__ == '__main__':
    main()
