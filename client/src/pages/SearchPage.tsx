import React, { useState } from 'react';
import { api } from '../services/api';
import { ProductCard } from '../components/ProductCard';
import '../styles/Search.css';

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
}

export const SearchPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState<SearchResults>({ olx: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchTerm.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const response = await api.search(searchTerm);
      // Ensure we have valid data before updating state
      if (response.data && Array.isArray(response.data.olx)) {
        setResults({ olx: response.data.olx });
      } else {
        setResults({ olx: [] });
        setError('No results found');
      }
    } catch (error) {
      console.error('Search failed:', error);
      setResults({ olx: [] });
      setError('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-page">
      <div className="search-container">
        <h1>PC Part Searcher</h1>
        <form onSubmit={handleSearch}>
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
        </form>
        {error && <div className="error-message">{error}</div>}
      </div>

      {loading && <div className="loader">Searching...</div>}

      {!loading && results.olx.length > 0 && (
        <div className="results-container">
          <h2>Search Results from OLX</h2>
          <div className="results-grid">
            {results.olx.map((item, index) => (
              <ProductCard
                key={`${item['Product ID'] || index}`}
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
    </div>
  );
};

export default SearchPage;
