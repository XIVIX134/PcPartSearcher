import { useState, useMemo, useCallback, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { searchProducts } from '../services/api';
import { ProductCard } from '../components/ProductCard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { SourceFilters } from '../components/SourceFilters';
import type { Product, SourceType, StockFilter as StockFilterType } from '../types';
import '../styles/Search.css';
import { generateUID } from '../utils/uid';
import { FiltersBar } from '../components/FiltersBar';
import { AdvancedSearchModal } from '../components/AdvancedSearchModal';
import { getCookie } from '../utils/cookies';

interface SourceFilters {
  olx: boolean;
  badr: boolean;
  sigma: boolean;
  amazon: boolean;
}

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
    amazon: true
  });
  const [stockFilter, setStockFilter] = useState<StockFilterType>('all');
  const [isFiltersVisible, setIsFiltersVisible] = useState(false);
  const [gridSize, setGridSize] = useState(4);
  const [isAdvancedSearchOpen, setIsAdvancedSearchOpen] = useState(false);

  const { data, isLoading, error } = useQuery({
    queryKey: ['search', submittedTerm, sourceFilters],
    queryFn: async () => {
      setIsSearching(true);
      try {
        return await searchProducts({ searchTerm: submittedTerm, sourceFilters });
      } finally {
        setIsSearching(false);
      }
    },
    enabled: submittedTerm.length > 2,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchTerm.trim().length > 2) {
      setSubmittedTerm(searchTerm);
    }
  };

  const handleFilterChange = (source: SourceType) => {
    setSourceFilters(prev => ({
      ...prev,
      [source]: !prev[source]
    }));
  };

  const sortProducts = useCallback((products: Product[]) => {
    // Reset to first page when sorting changes
    setCurrentPage(1);
    
    return [...products].sort((a, b) => {
      if (sortOption === 'newest') return 0;
      
      // Remove currency symbols and commas, then convert to number
      const priceA = parseFloat(a.Price.replace(/[^\d.]/g, '')) || 0;
      const priceB = parseFloat(b.Price.replace(/[^\d.]/g, '')) || 0;
      
      return sortOption === 'price-asc' ? priceA - priceB : priceB - priceA;
    });
  }, [sortOption]);

  // Process and sort all products first
  const processedProducts = useMemo(() => {
    let filteredProducts: Product[] = [
      ...(sourceFilters.olx ? data?.olx?.map(product => ({ 
        ...product, 
        source: 'olx' as const,
        uid: generateUID() 
      })) || [] : []),
      ...(sourceFilters.badr ? data?.badr?.map(product => ({ 
        ...product, 
        source: 'badr' as const,
        uid: generateUID()
      })) || [] : []),
      ...(sourceFilters.sigma ? data?.sigma?.map(product => ({ 
        ...product, 
        source: 'sigma' as const,
        uid: generateUID()
      })) || [] : []),
      ...(sourceFilters.amazon ? data?.amazon?.map(product => ({ 
        ...product, 
        source: 'amazon' as const,
        uid: generateUID()
      })) || [] : [])
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

    return sortProducts(filteredProducts);
  }, [data, sortProducts, sourceFilters, stockFilter]); // Re-sort when data or sortProducts changes

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
                Search
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
      <AdvancedSearchModal
        isOpen={isAdvancedSearchOpen}
        onClose={() => setIsAdvancedSearchOpen(false)}
        sourceFilters={sourceFilters}
        onSourceFilterChange={handleFilterChange}
        onSearch={handleSubmit}
      />
    </div>
  );
};