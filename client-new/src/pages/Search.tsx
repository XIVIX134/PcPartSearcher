import { useState, useMemo, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { searchProducts } from '../services/api';
import { ProductCard } from '../components/ProductCard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { SortControls } from '../components/SortControls';
import { ViewToggle } from '../components/ViewToggle';
import type { Product } from '../types';
import '../styles/Search.css';
import { generateUID } from '../utils/uid';

export const SearchPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [submittedTerm, setSubmittedTerm] = useState('');
  const [sortOption, setSortOption] = useState<'price-asc' | 'price-desc' | 'newest'>('newest');
  const [view, setView] = useState<'grid' | 'list'>('grid');
  const [isSearching, setIsSearching] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);

  const pages = [1, ...Array.from({ length: 14 }, (_, i) => i + 2)]; // pages 1-15

  const { data, isLoading, error } = useQuery({
    queryKey: ['search', submittedTerm],
    queryFn: async () => {
      setIsSearching(true);
      try {
        return await searchProducts(submittedTerm, pages);
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
    return sortProducts([
      ...(data?.olx?.map(product => ({ 
        ...product, 
        source: 'olx' as const,
        uid: generateUID() 
      })) || []),
      ...(data?.badr?.map(product => ({ 
        ...product, 
        source: 'badr' as const,
        uid: generateUID()
      })) || [])
    ] as Product[]);
  }, [data, sortProducts]); // Re-sort when data or sortProducts changes

  // Then paginate the sorted results
  const paginatedProducts = useMemo(() => {
    const startIndex = (currentPage - 1) * 24;
    const endIndex = startIndex + 24;
    return processedProducts.slice(startIndex, endIndex);
  }, [processedProducts, currentPage]);

  const totalPages = Math.ceil(processedProducts.length / 24);
  const hasResults = processedProducts.length > 0;

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
            <button type="submit" className="search-button" disabled={isLoading}>
              Search
            </button>
          </div>
        </form>

        {(isLoading || isSearching) && (
          <div className="loader-container">
            <LoadingSpinner size="large" />
            {isSearching && <p className="search-status">Searching multiple pages...</p>}
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
              <h2>Found {processedProducts.length} items</h2>
              <div className="results-controls">
                <SortControls
                  onSort={setSortOption}
                  currentSort={sortOption}
                />
                <ViewToggle 
                  view={view}
                  onViewChange={setView}
                />
              </div>
            </div>
            <div className={`results-${view}`}>
              {paginatedProducts.map((product) => (
                <ProductCard 
                  key={product.uid} 
                  product={product} 
                />
              ))}
            </div>
            {totalPages > 1 && (
              <div className="pagination">
                <button 
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                >
                  Previous
                </button>
                <span>{currentPage} of {totalPages}</span>
                <button 
                  onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                >
                  Next
                </button>
              </div>
            )}
          </div>
        )}

        {!isLoading && !hasResults && submittedTerm && (
          <div className="no-results">
            No products found for "{submittedTerm}"
          </div>
        )}
      </div>
    </div>
  );
};