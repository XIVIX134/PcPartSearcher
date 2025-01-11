export interface Product {
  'Product ID': string;
  'Title': string;
  'Price': string;
  'Tax': string;
  'Location': string;
  'Details Link': string;
  'Image URL': string;
  'Stock': string;
  'Brand': string;
  'Model': string;
  'Labels': string[];
  'Rating': number;
  'Description': string;
  'Page': number;
  
  source: SourceType;
  uid: string;
}

export interface SearchResponse {
  olx: Product[];
  badr: Product[];
  sigma: Product[];
  amazon: Product[];
  alfrensia: Product[];
  totalPages: number;
  itemsPerPage: number;
  status: string;
}

export type SourceType = 'olx' | 'badr' | 'sigma' | 'amazon' | 'alfrensia';

export type SourceFilters = {
  [key in SourceType]: boolean;
};

export type StockFilter = 'all' | 'in-stock' | 'out-of-stock';