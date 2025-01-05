import axios from 'axios';
import type { SearchResponse } from '../types';

const api = axios.create({
  baseURL: '/api',
  timeout: 60000, // Increased timeout for multiple pages
});

export const searchProducts = async (
  searchTerm: string,
  pages: number[] = [1]
): Promise<SearchResponse> => {
  try {
    // Send single request with all pages
    const response = await api.post<SearchResponse>('/search', { 
      searchTerm,
      pages
    });
    
    return response.data;
  } catch (error) {
    console.error('Search error:', error);
    throw error;
  }
};
