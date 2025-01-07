import { useState } from 'react';
import '@styles/PriceRangeFilter.css';

interface PriceRangeFilterProps {
  onFilterChange: (min: number, max: number) => void;
  min: number;
  max: number;
}

export const PriceRangeFilter = ({ onFilterChange, min, max }: PriceRangeFilterProps) => {
  const [minPrice, setMinPrice] = useState(min);
  const [maxPrice, setMaxPrice] = useState(max);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onFilterChange(minPrice, maxPrice);
  };

  return (
    <form className="price-filter" onSubmit={handleSubmit}>
      <div className="price-inputs">
        <input
          type="number"
          value={minPrice}
          onChange={(e) => setMinPrice(Number(e.target.value))}
          placeholder="Min"
          min={0}
        />
        <span>to</span>
        <input
          type="number"
          value={maxPrice}
          onChange={(e) => setMaxPrice(Number(e.target.value))}
          placeholder="Max"
          min={0}
        />
      </div>
      <button type="submit">Apply</button>
    </form>
  );
};
