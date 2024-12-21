import React, { useState } from 'react';
import { api } from '../services/api';
import { ProductCard } from '../components/ProductCard';
import '../styles/Search.css';

export const SearchPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState<{olx: any[], badr: any[]}>({ olx: [], badr: [] });
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchTerm.trim()) return;

    setLoading(true);
    try {
      const response = await api.search(searchTerm);
      setResults(response.data);
    } catch (error) {
      console.error('Search failed:', error);
    }
    setLoading(false);
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
      </div>

      {loading && <div className="loader">Searching...</div>}

      {!loading && (results.olx.length > 0) && (
        <div className="results-container">
          <h2>Search Results</h2>
          <div className="results-grid">
            {[...results.olx].map((item, index) => (
              <ProductCard
                key={`${item['Product ID']}-${index}`}
                title={item.Title}
                price={item.Price}
                location={item.Location}
                imageUrl={item['Image URL']}
                detailsLink={item['Details Link']}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
