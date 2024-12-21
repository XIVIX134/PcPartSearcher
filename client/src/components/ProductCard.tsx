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
    <div className="product-card">
      <img src={imageUrl} alt={title} />
      <h3>{title}</h3>
      <p>Price: {price}</p>
      {location && <p>Location: {location}</p>}
      <a href={detailsLink} target="_blank" rel="noopener noreferrer">
        View Details
      </a>
    </div>
  );
};
