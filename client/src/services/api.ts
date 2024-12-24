import axios from 'axios';

// Create axios instance with proxy configuration
const api = axios.create({
  baseURL: '/api',  // Use relative path - will be handled by Vite proxy
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
  withCredentials: false  // Changed to false to work with wildcard CORS
});

interface Product {
  'Product ID': string;
  'Title': string;
  'Price': string;
  'Location': string;
  'Image URL': string;
  'Details Link': string;
}

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  async (err) => {
    const { config, message } = err;
    if (!config || !config.retry) {
      return Promise.reject(err);
    }
    
    // Set the retry count
    config.retryCount = config.retryCount ?? 0;
    
    if (config.retryCount >= 3) {
      return Promise.reject(err);
    }
    
    // Increase the retry count
    config.retryCount += 1;
    
    // Create new promise to handle retry
    const backoff = new Promise(resolve => {
      setTimeout(() => resolve(null), 1000 * config.retryCount);
    });
    
    // Wait for backoff time, then retry
    await backoff;
    return api(config);
  }
);

export const apiService = {
  getSigmaItems: () => 
    api.get<{sigma_items: string[]}>('sigma/items'),
    
  search: (searchTerm: string) => 
    api.post('search', { searchTerm }, { 
      retry: true,
      timeout: 30000
    }),  // Use relative path
};
