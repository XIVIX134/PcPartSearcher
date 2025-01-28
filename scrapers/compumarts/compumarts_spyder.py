import httpx
from bs4 import BeautifulSoup
import json

search_term = "rtx"
url = f"https://www.compumarts.com/search?q={search_term}&options%5Bprefix%5D=last&type=product"

response = httpx.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

product_list = soup.find('ul', class_='productListing productGrid column-3 list-3 list-unstyled')

product_list_items = product_list.find_all('li', class_='product')

for product_div in product_list_items:

    data_product_id = product_div.get("data-product-id")
    data_json_product = product_div.get("data-json-product")
    
    # Parse the JSON product data
    product_data = json.loads(data_json_product) if data_json_product else {}

    # first one in srcset
    img_tag = product_div.find("img")
    image_url = img_tag.get("data-srcset").split(",")[0].split(" ")[0] if img_tag else None

    product_name = product_data.get("variants", [{}])[0].get("name", "N/A")
    product_price = product_data.get("variants", [{}])[0].get("price", "N/A")

    print("Product ID:", data_product_id)
    print("Product Name:", product_name)
    print("Product Price:", product_price)
    print("Image URL:", image_url)