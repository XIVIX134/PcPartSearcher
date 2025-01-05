import type { Product } from '../types';
import '../styles/ProductCard.css';

interface ProductCardProps {
  product: Product;
}

export const ProductCard = ({ product }: ProductCardProps) => {
  return (
    <a 
      href={product['Details Link']} 
      target="_blank" 
      rel="noopener noreferrer" 
      className="product-card"
    >
      <div className="product-image">
        <img src={product['Image URL']} alt={product.Title} />
      </div>
      <div className="product-info">
        <h3>{product.Title}</h3>
        <p className="price">{product.Price}</p>
        <p className="location">{product.Location}</p>
      </div>
    </a>
  );
};
