import requests
from bs4 import BeautifulSoup
import json
import re

# Sanitize the search term for use in filenames
def sanitize_filename(search_term):
    return re.sub(r'[^\w\-]', '_', search_term)

def scrape_sigma_computer(search_term):
    # Define the search URL with the search term
    base_url = "https://www.sigma-computer.com/search"
    params = {
        "search": search_term,
        "submit_search": "",
        "route": "product/search"
    }
    
    # Send a GET request
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all product blocks
    product_blocks = soup.find_all("div", class_="product-layout")
    
    # Extract product details
    results = []
    for product in product_blocks:
        try:
            title = product.find("h4").text.strip()
            link = product.find("h4").find("a")["href"]
            image = product.find("img", class_="img-1")["src"]
            price_new = product.find("span", class_="price-new").text.strip()
            price_old = product.find("span", class_="price-old").text.strip() if product.find("span", class_="price-old") else None
            
            description_elements = product.find("div", class_="description").find_all("div")
            description = "\n".join([desc.text.strip() for desc in description_elements if desc.text.strip()])
            
            # Improved stock detection
            stock_status = "Unknown"
            stock_element = product.find("span", class_="stock")
            if stock_element:
                status_text = stock_element.text.strip().lower()
                if "متوفر" in status_text or "in stock" in status_text:
                    stock_status = "In Stock"
                elif "غير متوفر" in status_text or "out of stock" in status_text:
                    stock_status = "Out of Stock"
                else:
                    # Try alternative stock indicator
                    stock_span = product.find("span", class_="stock_Y") or product.find("span", class_="stock_N")
                    if stock_span:
                        if "stock_Y" in stock_span.get("class", []):
                            stock_status = "In Stock"
                        elif "stock_N" in stock_span.get("class", []):
                            stock_status = "Out of Stock"
            
            # Append to results with improved stock status
            results.append({
                "title": title,
                "link": f"https://www.sigma-computer.com/{link}",
                "image": f"https://www.sigma-computer.com/{image}",
                "price_new": price_new,
                "price_old": price_old,
                "stock": stock_status,
                "description": description
            })
        except Exception as e:
            print(f"Error parsing product: {e}")
    
    return results

def main(search_term):
    data = scrape_sigma_computer(search_term)

    # Generate the file name
    result_file = f"{sanitize_filename(search_term)}.json"

    # Save the results to a JSON file
    if data:
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Data saved to {result_file}")

if __name__ == "__main__":
    main("rtx")