import * as React from 'react';
import { useState, FormEvent } from 'react';
import { apiService } from '../services/api';
import { ProductCard } from '../components/ProductCard';
import '../styles/Search.css';

type SortDirection = 'asc' | 'desc' | null;

interface Product {
  'Product ID': string;
  'Title': string;
  'Price': string;
  'Location': string;
  'Image URL': string;
  'Details Link': string;
}

interface SearchResults {
  olx: Product[]; 
  badr: any[];
}

export const SearchPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState<SearchResults>({ olx: [], badr: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>(null);
  const [hasResults, setHasResults] = useState(false);

  const handleSearch = async (e: FormEvent) => {
    e.preventDefault();
    if (!searchTerm.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const response = await apiService.search(searchTerm);
      // Make sure response data matches the expected structure
      if (response.data && Array.isArray(response.data.olx)) {
        setResults({
          olx: response.data.olx,
          badr: response.data.badr || []
        });
        setHasResults(response.data.olx.length > 0);
      } else {
        setResults({ olx: [], badr: [] });
        setError('No results found');
        setHasResults(false);
      }
    } catch (err) {
      console.error('Search failed:', err);
      setResults({ olx: [], badr: [] });
      setError('Search failed. Please try again.');
      setHasResults(false);
    } finally {
      setLoading(false);
    }
  };

  const sortResults = (direction: SortDirection) => {
    if (!results.olx.length) return;
    setSortDirection(direction);
    const sorted = [...results.olx].sort((a, b) => {
      const priceA = parseFloat(a.Price.replace(/[^0-9.]/g, ''));
      const priceB = parseFloat(b.Price.replace(/[^0-9.]/g, ''));
      return direction === 'asc' ? priceA - priceB : priceB - priceA;
    });
    setResults({ ...results, olx: sorted });
  };

  return (
    <div className="search-page">
      <div className={`search-container ${hasResults ? 'has-results' : ''}`}>
        <h1>PC Part Searcher</h1>
        <form onSubmit={handleSearch}>
          <div className={`input-container ${hasResults ? 'expanded' : ''}`}>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search for PC parts..."
              className="search-input"
            />
            <button type="submit" className="search-button" disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </form>
      </div>

      {loading && <div className="loader">Searching...</div>}

      {!loading && results.olx.length > 0 && (
        <div className={`results-container ${results.olx.length > 0 ? 'visible' : ''}`}>
          <div className="results-header">
            <h2>Search Results ({results.olx.length} items)</h2>
            <div className="sort-controls">
              <select
                className="sort-select"
                aria-label="Sort results by price"
                onChange={(e) => sortResults(e.target.value as SortDirection)}
                value={sortDirection || ''}
              >
                <option value="" disabled selected hidden>Sort by price</option>
                <option value="asc">Price: Low to High</option>
                <option value="desc">Price: High to Low</option>
              </select>
            </div>
          </div>

          <div className="results-grid">
            {results.olx.map((item, index) => (
              <ProductCard
                key={`${item['Product ID'] || 'item'}-${index}`}
                title={item.Title || 'No Title'}
                price={item.Price || 'No Price'}
                location={item.Location || 'No Location'}
                imageUrl={item['Image URL'] || ''}
                detailsLink={item['Details Link'] || '#'}
              />
            ))}
          </div>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}
    </div>
  );
};
