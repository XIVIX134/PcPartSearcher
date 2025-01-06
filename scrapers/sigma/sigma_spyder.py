import requests
from bs4 import BeautifulSoup
import json

# Motherboards URL
url = "https://www.sigma-computer.com/subcategory?id=1&cname=Desktop&id2=1&scname=Motherboard"

# GPUs URL
url2 = "https://www.sigma-computer.com/subcategory?id=1&cname=Desktop&id2=2&scname=Graphic%20Card"

# User-Agent for HTTP headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Change the URL here as needed
response = requests.get(url2, headers=headers)
response.raise_for_status()

# Parse the response content
soup = BeautifulSoup(response.content, "html.parser")

# Find all products
products = soup.find_all("div", class_="product-layout")

# List to store product data
product_data = []

for product in products:
    # Extract product name
    name = product.find("h4").text.strip() if product.find("h4") else "N/A"

    # Extract product price
    price_tag = product.find("span", class_="price-new")
    price = price_tag.text.strip() if price_tag else "N/A"

    # Extract product image URL
    image_tag = product.find("img", class_="img-1")
    image_url = f"https://www.sigma-computer.com/{image_tag['src']}" if image_tag else "N/A"

    # Extract product link
    link_tag = product.find("a", href=True)
    product_link = f"https://www.sigma-computer.com/{link_tag['href']}" if link_tag else "N/A"

    # Extract product description
    description_tag = product.find("div", class_="description")
    description = description_tag.text.strip() if description_tag else "N/A"

    # Add product details to the list
    product_data.append({
        "name": name,
        "price": price,
        "image_url": image_url,
        "product_link": product_link,
        "description": description
    })

# Save data to a JSON file
if product_data:
    with open("sigma_result.json", "w", encoding="utf-8") as f:
        json.dump(product_data, f, ensure_ascii=False, indent=4)

    print("Data saved to sigma_result.json")
else:
    print("No data to save.")
