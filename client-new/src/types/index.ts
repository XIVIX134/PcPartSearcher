export interface Product {
  'Product ID': string;
  'Title': string;
  'Price': string;
  'Location': string;
  'Image URL': string;
  'Details Link': string;
  source: 'olx' | 'badr' | 'sigma';  // Add sigma as a source
  uid: string;  // Add uid field
}

export interface SearchResponse {
  olx: Product[];
  badr: Product[];
  sigma: Product[];  // Add sigma results
  totalPages: number;
  itemsPerPage: number;
}

export type SourceType = 'olx' | 'badr' | 'sigma';

export type SourceFilters = {
  [key in SourceType]: boolean;
};
