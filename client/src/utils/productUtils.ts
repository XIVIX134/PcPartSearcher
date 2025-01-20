import { Product, SourceType } from '../types';
import { generateUID } from './uid';

// Normalize product object to ensure consistent format
export const normalizeProduct = (product: Product, source: SourceType): Product => {
  return {
    ...product,
    source,
    uid: generateUID(),
    'Product ID': product['Product ID'] || generateUID(),
    'Price': formatPrice(normalizePrice(product.Price)),
    'Stock': normalizeStockStatus(product.Stock),
  };
};

// Convert price string to number for sorting/comparison
export const normalizePrice = (price?: string): number => {
  if (!price) return 0;
  // Remove currency symbols, commas, and other non-numeric characters except decimal point
  const cleanPrice = price.replace(/[^0-9.]/g, '');
  const number = parseFloat(cleanPrice);
  return isNaN(number) ? 0 : number;
};

// Normalize stock status strings
const normalizeStockStatus = (stock?: string): string => {
  if (!stock) return 'Unknown';
  
  const status = stock.toLowerCase();
  if (status.includes('in stock') || status === 'instock') {
    return 'In Stock';
  }
  if (status.includes('out') || status === 'outofstock') {
    return 'Out of Stock';
  }
  return 'Unknown';
};

// Format price with currency
export const formatPrice = (price: number): string => {
  return `${price.toLocaleString('en-US')} EGP`;
};
