import axios from 'axios';

const API_URL = 'http://localhost:5000';

interface Product {
  'Product ID': string;
  'Title': string;
  'Price': string;
  'Location': string;
  'Image URL': string;
  'Details Link': string;
}

export const api = {
  getSigmaItems: () => axios.get<{sigma_items: string[]}>(`${API_URL}/sigma/items`),
  search: (searchTerm: string) => 
    axios.post<{olx: Product[], badr: Product[]}>(`${API_URL}/search`, { searchTerm }),
};
