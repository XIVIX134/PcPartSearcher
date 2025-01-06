import axios from 'axios';
import type { SearchResponse } from '../types';

const api = axios.create({
  baseURL: '/api', // Use relative path for proxy
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
  withCredentials: false
});

// Add request/response interceptors
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

export const searchProducts = async (searchTerm: string): Promise<SearchResponse> => {
  try {
    console.log('Sending search request for:', searchTerm);
    const response = await api.post('/search', { searchTerm });
    return response.data;
  } catch (error: unknown) {
    console.error('Search error:', error);
    if (axios.isAxiosError(error)) {
      if (error.response) {
        // Server responded with error
        throw new Error(error.response.data.message || 'Server error');
      } else if (error.request) {
        // Request made but no response
        throw new Error('No response from server');
      }
    }
    throw error;
  }
};
