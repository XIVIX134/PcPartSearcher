export interface Product {
  'Product ID': string;
  'Title': string;
  'Price': string;
  'Location': string;
  'Image URL': string;
  'Details Link': string;
  source: SourceType;
  uid: string;
  stock?: string;
  Description?: string;
  rating?: string;
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

export interface Filters {
  sources: SourceFilters;
  stock: StockFilter;
}

export interface SearchState {
  currentTerm: string;
  searchedSources: Record<SourceType, boolean>;
  isPartialSearching: boolean;
}

export interface AdvancedSearchState {
  tempFilters: SourceFilters;
  pendingSources: SourceType[];
}
