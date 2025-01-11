import type { Product } from '../types';
import '../styles/ProductCard.css';

interface ProductCardProps {
  product: Product;  // Explicitly type the product prop
}

export const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const getStockClass = (stockStatus: string | undefined) => {
    if (!stockStatus) return 'out-stock';
    const status = stockStatus.toLowerCase();
    if (status.includes('in stock')) return 'in-stock';
    return 'out-stock';  // Both unknown and out of stock return out-stock
  };

  const getStockDisplay = (stockStatus: string | undefined) => {
    if (!stockStatus || stockStatus === 'Unknown') return 'Out of Stock';
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
              <span className={`stock-badge ${getStockClass(product.Stock)}`}>
                {getStockDisplay(product.Stock)}
              </span>
            )}
            {product.source === 'amazon' && product.Rating && (
              <span className="rating-badge">
                {product.Rating}
              </span>
            )}
          </div>
        </div>
      </a>
    </div>
  );
};
