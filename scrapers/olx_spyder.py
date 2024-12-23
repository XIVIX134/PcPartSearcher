import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import quote

# Base URL for details
BASE_URL = "https://www.dubizzle.com.eg"

def scrape_olx(search_term=None):
    """
    Scrapes OLX listings with optional search term
    Args:
        search_term (str): Optional search term to filter results
    """
    # Construct URL based on search term
    if search_term:
        # Replace spaces with hyphens and encode
        processed_term = search_term.replace(' ', '-')
        encoded_term = quote(processed_term)
        url = f"https://www.dubizzle.com.eg/en/electronics-home-appliances/computers-accessories/q-{encoded_term}/"
    else:
        url = "https://www.dubizzle.com.eg/en/electronics-home-appliances/computers-accessories/"

    # Initialize an empty list to store the data
    data_list = []

    # Fetch the page content
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all listings
        listings = soup.find_all('li', attrs={'aria-label': 'Listing'})
        
        for listing in listings:
            # Extract the title
            title_tag = listing.find('h2', class_='_941ffa5e')
            title = title_tag.text.strip() if title_tag else "N/A"
            
            # Extract the price
            price_tag = listing.find('span', class_='_1f2a2b47')
            price = price_tag.text.strip() if price_tag else "N/A"
            
            # Extract the location
            location_tag = listing.find('span', class_='_77000f35')
            location = location_tag.text.strip() if location_tag else "N/A"
            
            # Extract the image URL
            image_tag = listing.find('img', class_='f79152f1')
            image_url = image_tag['src'] if image_tag else "N/A"
            
            # Extract the link to details and product ID
            link_tag = listing.find('a', href=True)
            if link_tag:
                details_link = BASE_URL + link_tag['href']
                # Extract product ID from the URL
                match = re.search(r'-ID(\d+)', link_tag['href'])
                product_id = match.group(1) if match else "N/A"
            else:
                details_link = "null"
                product_id = "null"
            
            # Add the extracted data to the list
            data_list.append({
                "Product ID": product_id,
                "Title": title,
                "Price": price,
                "Location": location,
                "Image URL": image_url,
                "Details Link": details_link,
            })
        
            print(f"Found {len(data_list)} listings")
            return data_list
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return []

if __name__ == '__main__':
    # Example searches without spaces
    scrape_olx("Laptop")
    # Example searches with spaces
    scrape_olx("RTX 3080")
