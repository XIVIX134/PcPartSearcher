import requests
from bs4 import BeautifulSoup

# motherboards
url = "https://www.sigma-computer.com/subcategory?id=1&cname=Desktop&id2=1&scname=Motherboard"

#GPUs
url2 = "https://www.sigma-computer.com/subcategory?id=1&cname=Desktop&id2=2&scname=Graphic%20Card"


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
response = requests.get(url2, headers=headers)
response.raise_for_status()


soup = BeautifulSoup(response.content, "html.parser")


products = soup.find_all("div", class_="product-layout")


for product in products:
    
    name = product.find("h4").text.strip() if product.find("h4") else "N/A"
    
   
    price_tag = product.find("span", class_="price-new")
    price = price_tag.text.strip() if price_tag else "N/A"
    
    
    image_tag = product.find("img", class_="img-1")
    image_url = f"https://www.sigma-computer.com/{image_tag['src']}" if image_tag else "N/A"
    
    
    link_tag = product.find("a", href=True)
    product_link = f"https://www.sigma-computer.com/{link_tag['href']}" if link_tag else "N/A"
    
    
    description_tag = product.find("div", class_="description")
    description = description_tag.text.strip() if description_tag else "N/A"
    
    
    print(f"Name: {name}")
    print(f"Price: {price}")
    print(f"Image URL: {image_url}")
    print(f"Product Link: {product_link}")
    print(f"Description: {description}")
    print("-" * 50)
