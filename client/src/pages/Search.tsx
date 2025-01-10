import { useState, useMemo, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { searchProducts } from '../services/api';
import { ProductCard } from '../components/ProductCard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { SourceFilters } from '../components/SourceFilters';
import type { Product, SourceType, StockFilter as StockFilterType } from '../types';
interface SearchResponse {
  olx: Product[];
  badr: Product[];
  sigma: Product[];
  amazon: Product[];
  alfrensia: Product[];
  totalPages: number;
  itemsPerPage: number;
  status: string;
}
import '../styles/Search.css';
import { FiltersBar } from '../components/FiltersBar';
import { AdvancedSearchModal } from '../components/AdvancedSearchModal';
import { getCookie } from '../utils/cookies';
import { normalizeProduct, normalizePrice } from '../utils/productUtils';

type SourceFilters = Record<SourceType, boolean>;

export const SearchPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [submittedTerm, setSubmittedTerm] = useState('');
  const [sortOption, setSortOption] = useState<'price-asc' | 'price-desc' | 'newest'>('newest');
  const [view, setView] = useState<'grid' | 'list'>('grid');
  const [isSearching, setIsSearching] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [sourceFilters, setSourceFilters] = useState<SourceFilters>({
    olx: true,
    badr: true,
    sigma: true,
    amazon: true,
    alfrensia: true
  });
  const [stockFilter, setStockFilter] = useState<StockFilterType>('all');
  const [isFiltersVisible, setIsFiltersVisible] = useState(false);
  const [gridSize, setGridSize] = useState(4);
  const [isAdvancedSearchOpen, setIsAdvancedSearchOpen] = useState(false);

  // Keep track of which sources have been searched
  const [searchedSources, setSearchedSources] = useState<Record<SourceType, boolean>>({
    olx: false,
    badr: false,
    sigma: false,
    amazon: false,
    alfrensia: false
  });
  const [isPartialSearching] = useState(false);
  const [lastSearchTerm, setLastSearchTerm] = useState('');


  // Update handleFilterChange to handle both single source and full filters updates
  const handleFilterChange = (newFilters: Record<SourceType, boolean> | SourceType) => {
    if (typeof newFilters === 'string') {
      // Handle single source toggle
      setSourceFilters(prev => ({
        ...prev,
        [newFilters]: !prev[newFilters]
      }));
    } else {
      // Handle full filters update
      setSourceFilters(newFilters);
    }
  };

  // Modify useQuery to only search new sources
  const { data, isLoading, error } = useQuery({
    queryKey: ['search', submittedTerm, sourceFilters],
    queryFn: async () => {
      setIsSearching(true);
      try {
        // Only include sources that haven't been searched yet
        const sourcesToSearch = Object.entries(sourceFilters)
          .filter(([source, enabled]) => {
            const sourceKey = source as SourceType;
            return enabled && !searchedSources[sourceKey];
          })
          .reduce((acc, [source]) => ({ ...acc, [source]: true }), {});

        // If no new sources to search, return empty results
        if (Object.keys(sourcesToSearch).length === 0) {
          return allResults; // Return existing results instead of empty ones
        }

        const response = await searchProducts({ 
          searchTerm: submittedTerm.trim(),
          sourceFilters: sourcesToSearch,
          isPartial: true  // Add this flag
        });

        // Mark searched sources
        const newSearchedSources = { ...searchedSources };
        Object.keys(sourcesToSearch).forEach(source => {
          newSearchedSources[source as SourceType] = true;
        });
        setSearchedSources(newSearchedSources);

        return response;
      } catch (err) {
        console.error('Search error:', err);
        throw new Error(err instanceof Error ? err.message : 'Search failed');
      } finally {
        setIsSearching(false);
      }
    },
    enabled: submittedTerm.trim().length > 2,
  });

  // Reset searched sources when search term changes
  useEffect(() => {
    setSearchedSources({
      olx: false,
      badr: false,
      sigma: false,
      amazon: false,
      alfrensia: false
    });
    // Also reset all results
    setAllResults({
      olx: [],
      badr: [],
      sigma: [],
      amazon: [],
      alfrensia: [],
      totalPages: 0,
      itemsPerPage: 24,
      status: 'idle'
    });
  }, [submittedTerm]);

  // Store all fetched results separately
  const [allResults, setAllResults] = useState<SearchResponse>({
    olx: [],
    badr: [],
    sigma: [],
    amazon: [],
    alfrensia: [],
    totalPages: 0,
    itemsPerPage: 24,
    status: 'idle'
  });

  // Update allResults when new data arrives
  useEffect(() => {
    if (data) {
      setAllResults((prev: SearchResponse) => {
        // Create a new results object
        const newResults = { ...prev };
        
        // Only update arrays that have new data
        // This prevents duplicate entries when toggling sources
        if (data.olx?.length) newResults.olx = data.olx;
        if (data.badr?.length) newResults.badr = data.badr;
        if (data.sigma?.length) newResults.sigma = data.sigma;
        if (data.amazon?.length) newResults.amazon = data.amazon;
        if (data.alfrensia?.length) newResults.alfrensia = data.alfrensia;

        return {
          ...newResults,
          totalPages: data.totalPages || prev.totalPages,
          itemsPerPage: data.itemsPerPage || prev.itemsPerPage,
          status: data.status || prev.status
        };
      });
    }
  }, [data]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchTerm.trim().length > 2) {
      // If search term changed, reset searched sources
      if (searchTerm !== lastSearchTerm) {
        setSearchedSources(Object.fromEntries(
          Object.keys(sourceFilters).map(source => [source as SourceType, false])
        ) as Record<SourceType, boolean>);
        setAllResults({
          olx: [], badr: [], sigma: [], amazon: [], alfrensia: [],
          totalPages: 0, itemsPerPage: 24, status: 'idle'
        });
      }
      setLastSearchTerm(searchTerm);
      setSubmittedTerm(searchTerm);
    }
  };

  // Process and sort all products first
  const processedProducts = useMemo(() => {
    let filteredProducts: Product[] = [
      ...(sourceFilters.olx ? allResults?.olx?.map(product => normalizeProduct(product, 'olx')) || [] : []),
      ...(sourceFilters.badr ? allResults?.badr?.map(product => normalizeProduct(product, 'badr')) || [] : []),
      ...(sourceFilters.sigma ? allResults?.sigma?.map(product => normalizeProduct(product, 'sigma')) || [] : []),
      ...(sourceFilters.amazon ? allResults?.amazon?.map(product => normalizeProduct(product, 'amazon')) || [] : []),
      ...(sourceFilters.alfrensia ? allResults?.alfrensia?.map(product => normalizeProduct(product, 'alfrensia')) || [] : []),
    ];

    // Apply stock filter
    if (stockFilter !== 'all') {
      filteredProducts = filteredProducts.filter(product => {
        const stockStatus = product.stock?.toLowerCase() || '';
        
        if (stockFilter === 'in-stock') {
          // For Sigma products, check stock status
          if (product.source === 'sigma') {
            return stockStatus.includes('in stock');
          }
          // For OLX products, consider them all in stock
          return product.source === 'olx';
        } else if (stockFilter === 'out-of-stock') {
          // Only show Sigma products that are explicitly out of stock
          return product.source === 'sigma' && !stockStatus.includes('in stock');
        }
        return true;
      });
    }

    // Update price comparison to use normalizer
    if (sortOption !== 'newest') {
      filteredProducts.sort((a, b) => {
        const priceA = normalizePrice(a.Price);
        const priceB = normalizePrice(b.Price);
        return sortOption === 'price-asc' ? priceA - priceB : priceB - priceA;
      });
    }

    return filteredProducts;
  }, [allResults, sourceFilters, sortOption, stockFilter]); // Re-sort when data or sortProducts changes

  // Then paginate the sorted results
  const paginatedProducts = useMemo(() => {
    const startIndex = (currentPage - 1) * 24;
    const endIndex = startIndex + 24;
    return processedProducts.slice(startIndex, endIndex);
  }, [processedProducts, currentPage]);

  const totalPages = Math.ceil(processedProducts.length / 24);
  const hasResults = processedProducts.length > 0;

  useEffect(() => {
    document.documentElement.style.setProperty('--grid-size', gridSize.toString());
  }, [gridSize]);

  // Modify the useEffect for resize handling
  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      // Only handle grid size on mobile
      if (width <= 768) {
        setGridSize(prevSize => Math.min(prevSize, 2));
      }
    };

    window.addEventListener('resize', handleResize);
    // Initial check
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Load preferences from cookies on mount
  useEffect(() => {
    const savedPreferences = getCookie('searchPreferences');
    if (savedPreferences) {
      if (savedPreferences.sourceFilters) {
        setSourceFilters(savedPreferences.sourceFilters);
      }
    }
  }, []);

  return (
    <div className="search-page">
      <div className={`search-container ${hasResults ? 'has-results' : ''}`}>
        <h1 className="title-glow">PC Part Searcher</h1>
        
        <form onSubmit={handleSubmit} className="search-form">
          <div className={`input-container ${hasResults ? 'expanded' : ''}`}>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search for PC parts..."
              className="search-input"
            />
            <div className="button-group">
              <button 
                type="button"
                className="advanced-search-button"
                onClick={() => setIsAdvancedSearchOpen(true)}
                title="Advanced Search"
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                >
                  <line x1="4" y1="21" x2="4" y2="14" />
                  <line x1="4" y1="10" x2="4" y2="3" />
                  <line x1="12" y1="21" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12" y2="3" />
                  <line x1="20" y1="21" x2="20" y2="16" />
                  <line x1="20" y1="12" x2="20" y2="3" />
                  <line x1="1" y1="14" x2="7" y2="14" />
                  <line x1="9" y1="8" x2="15" y2="8" />
                  <line x1="17" y1="16" x2="23" y2="16" />
                </svg>
              </button>
              <button type="submit" className="search-button" disabled={isLoading}>
                {isPartialSearching ? (
                  <>
                    Search
                    <LoadingSpinner size="small" />
                  </>
                ) : (
                  'Search'
                )}
              </button>
            </div>
          </div>
        </form>

        {(isLoading || isSearching) && (
          <div className="loader-container">
            <LoadingSpinner size="large" />
          </div>
        )}

        {error && (
          <div className="error-message">
            An error occurred while searching. Please try again.
          </div>
        )}

        {!isLoading && hasResults && (
          <div className={`results-container visible`}>
            <div className="results-header">
              <div className="header-left">
                <h2>Found {processedProducts.length} items</h2>
                <button 
                  className="filters-toggle"
                  onClick={() => setIsFiltersVisible(!isFiltersVisible)}
                >
                  {isFiltersVisible ? 'Hide Filters' : 'Show Filters'}
                </button>
              </div>
            </div>
            <div className={`results-layout ${isFiltersVisible ? 'with-filters' : ''}`}>
              <FiltersBar 
                className={isFiltersVisible ? 'visible' : ''}
                sourceFilters={sourceFilters}
                stockFilter={stockFilter}
                sortOption={sortOption}
                view={view}
                gridSize={gridSize}
                onSourceFilterChange={handleFilterChange}
                onStockFilterChange={setStockFilter}
                onSortChange={setSortOption}
                onViewChange={setView}
                onGridSizeChange={setGridSize}
                searchedSources={searchedSources} // Add this line
              />
              <div className="results-content">
                <div className={`results-${view}`}>
                  {paginatedProducts.map((product: Product) => (
                    <ProductCard 
                      key={product.uid} 
                      product={product} 
                    />
                  ))}
                </div>
                {totalPages > 1 && (
                  <div className="pagination">
                    <button 
                      onClick={() => setCurrentPage((p: number) => Math.max(1, p - 1))}
                      disabled={currentPage === 1}
                    >
                      Previous
                    </button>
                    <span>{currentPage} of {totalPages}</span>
                    <button 
                      onClick={() => setCurrentPage((p: number) => Math.min(totalPages, p + 1))}
                      disabled={currentPage === totalPages}
                    >
                      Next
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {!isLoading && !hasResults && submittedTerm && (
          <div className="no-results">
            No products found for "{submittedTerm}"
          </div>
        )}
      </div>
      {/* Move modal outside container */}
      <AdvancedSearchModal
        isOpen={isAdvancedSearchOpen}
        onClose={() => setIsAdvancedSearchOpen(false)}
        onSearch={() => handleSubmit({ preventDefault: () => {} } as React.FormEvent)}
        sourceFilters={sourceFilters}
        onSourceFilterChange={handleFilterChange}
        searchTerm={searchTerm}
        lastSearchTerm={lastSearchTerm}
        searchedSources={searchedSources}
      />
    </div>
  );
};