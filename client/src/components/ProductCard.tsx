import React from 'react';

interface ProductProps {
  title: string;
  price: string;
  location?: string;
  imageUrl: string;
  detailsLink: string;
}

export const ProductCard: React.FC<ProductProps> = ({
  title,
  price,
  location,
  imageUrl,
  detailsLink
}) => {
  return (
    <a 
      href={detailsLink} 
      target="_blank" 
      rel="noopener noreferrer" 
      className="product-card-link"
    >
      <div className="product-card">
        <img src={imageUrl} alt={title} />
        <h3>{title}</h3>
        {location && <p className="location">Location: {location}</p>}
        <p className="price">{price}</p>
      </div>
    </a>
  );
};
