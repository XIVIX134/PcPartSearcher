import axios, { AxiosError, AxiosRequestConfig } from 'axios';
import type { SearchResponse } from '../types';

const MAX_RETRIES = 3;
const RETRY_DELAY = 1000;

interface ExtendedAxiosRequestConfig extends AxiosRequestConfig {
  _retryCount?: number;
}

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000,
  withCredentials: false
});

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

api.interceptors.request.use(config => {
  console.log('>>> Sending request:', config.method?.toUpperCase(), config.url);
  return config;
});

api.interceptors.response.use(
  response => {
    console.log('<<< Received response:', response.status, response.config.url);
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as ExtendedAxiosRequestConfig;
    if (!originalRequest) {
      return Promise.reject(error);
    }

    // Add retry count to request config
    const retryCount = originalRequest._retryCount || 0;
    originalRequest._retryCount = retryCount;

    // If we still have retries left and it's a connection error, retry the request
    if (retryCount < MAX_RETRIES && (
      error.code === 'ECONNABORTED' ||
      error.code === 'ERR_NETWORK' ||
      error.message.includes('Network Error') ||
      error.message.includes('timeout')
    )) {
      originalRequest._retryCount = retryCount + 1;
      await sleep(RETRY_DELAY * (retryCount + 1));
      return api(originalRequest);
    }

    console.error('!!! Request failed:', {
      message: error.message,
      url: error.config?.url,
      status: error.response?.status,
      code: error.code
    });
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
    const response = await api.post<SearchResponse>('/search', {
      search_term: searchTerm,
      source_filters: sourceFilters,
      is_partial: isPartial
    });

    return {
      olx: response.data.olx || [],
      badr: response.data.badr || [],
      sigma: response.data.sigma || [],
      amazon: response.data.amazon || [],
      alfrensia: response.data.alfrensia || [],
      totalPages: response.data.totalPages || 1,
      itemsPerPage: response.data.itemsPerPage || 24,
      status: response.data.status || 'success'
    };
  } catch (error) {
    if (error instanceof AxiosError) {
      const errorMessage = error.code === 'ERR_NETWORK' 
        ? 'Unable to connect to the search service. Please check if the server is running.'
        : error.message;
      console.error('Search API Error:', errorMessage);
      throw new Error(errorMessage);
    }
    throw error;
  }
};
