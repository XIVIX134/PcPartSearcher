import type { Product } from '../types';
import '../styles/ProductCard.css';

interface ProductCardProps {
  product: Product;
  showWishlistButton?: boolean;
  onWishlistToggle?: (product: Product) => void;
  isInWishlist?: boolean;
}

export const ProductCard: React.FC<ProductCardProps> = ({ 
  product, 
  showWishlistButton = false,
  onWishlistToggle,
  isInWishlist = false
}) => {
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
      <div className="product-card main-card">
        {showWishlistButton && (
          <button 
            className={`wishlist-button ${isInWishlist ? 'active' : ''}`}
            onClick={() => onWishlistToggle?.(product)}
            aria-label={isInWishlist ? 'Remove from wishlist' : 'Add to wishlist'}
            type="button"
          >
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 24 24" 
              fill={isInWishlist ? 'currentColor' : 'none'}
              stroke="currentColor" 
              strokeWidth="2"
            >
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </button>
        )}
        <a 
          href={product['Details Link']} 
          target="_blank" 
          rel="noopener noreferrer" 
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
    </div>
  );
};
