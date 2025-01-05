export interface Product {
  'Product ID': string;
  'Title': string;
  'Price': string;
  'Location': string;
  'Image URL': string;
  'Details Link': string;
  source: 'olx' | 'badr';  // Make source required
  uid: string;  // Add uid field
}

export interface SearchResponse {
  olx: Product[];
  badr: Product[];
  totalPages: number;
  itemsPerPage: number;
}
