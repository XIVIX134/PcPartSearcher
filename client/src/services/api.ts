import axios from 'axios';
import type { SearchResponse } from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000,
  withCredentials: false
});

// TODO: in production remove console.log statements
api.interceptors.request.use(config => {
  console.log('>>> Sending request:', config.method?.toUpperCase(), config.url);
  return config;
});

api.interceptors.response.use(
  response => {
    console.log('<<< Received response:', response.status, response.config.url);
    return response;
  },
  error => {
    console.error('!!! Request failed:', error.message, error.config?.url);
    return Promise.reject(error);
  }
);

interface SearchParams {
  searchTerm: string;
  sourceFilters: Record<string, boolean>;
  isPartial?: boolean;
}

export const searchProducts = async ({ searchTerm, sourceFilters, isPartial = false }: SearchParams): Promise<SearchResponse> => {
  try {
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        search_term: searchTerm,
        source_filters: sourceFilters,
        is_partial: isPartial
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Ensure all arrays exist even if empty
    return {
      olx: data.olx || [],
      badr: data.badr || [],
      sigma: data.sigma || [],
      amazon: data.amazon || [],
      alfrensia: data.alfrensia || [],
      totalPages: data.total_pages || 1,
      itemsPerPage: data.items_per_page || 24,
      status: data.status || 'success'
    };
  } catch (error) {
    console.error('Search API Error:', error);
    throw error;
  }
};
