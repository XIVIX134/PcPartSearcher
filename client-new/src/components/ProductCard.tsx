import type { Product } from '../types';
import '../styles/ProductCard.css';

interface ProductCardProps {
  product: Product;
}

export const ProductCard = ({ product }: ProductCardProps) => {
  const getStockClass = (stockStatus: string | undefined) => {
    if (!stockStatus) return 'unknown';
    const status = stockStatus.toLowerCase();
    if (status.includes('in stock')) return 'in-stock';
    if (status.includes('out of stock')) return 'out-stock';
    return 'unknown';
  };

  const getStockDisplay = (stockStatus: string | undefined) => {
    if (!stockStatus || stockStatus === 'Unknown') return 'Status Unknown';
    return stockStatus;
  };

  return (
    <div className="card-container">
      {/* Image-only shadow card */}
      <div className="shadow-card">
        <img src={product['Image URL']} alt="" />
      </div>
      
      {/* Main card */}
      <a 
        href={product['Details Link']} 
        target="_blank" 
        rel="noopener noreferrer" 
        className="product-card main-card"
      >
        <div className="product-image">
          <img src={product['Image URL']} alt={product.Title} />
        </div>
        <div className="product-info">
          <h3>{product.Title}</h3>
          <p className="price">{product.Price}</p>
          <div className="card-footer">
            <p className="location">
              {product.Location}
              <span className="source-badge">
                {product.source.toUpperCase()}
              </span>
            </p>
            {product.source === 'sigma' && (
              <span className={`stock-badge ${getStockClass(product.stock)}`}>
                {getStockDisplay(product.stock)}
              </span>
            )}
          </div>
        </div>
      </a>
    </div>
  );
};
