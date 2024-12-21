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
  getLaptops: () => axios.get<Product[]>(`${API_URL}/olx/laptops`),
  getCPUs: () => axios.get<Product[]>(`${API_URL}/badr/cpus`),
  getSigmaItems: () => axios.get<{sigma_items: string[]}>(`${API_URL}/sigma/items`),
  search: (searchTerm: string) => 
    axios.post<{olx: Product[], badr: Product[]}>(`${API_URL}/search`, { searchTerm }),
};
