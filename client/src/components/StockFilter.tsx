import type { StockFilter as StockFilterType } from '../types';
import '../styles/StockFilter.css';

interface StockFilterProps {
  value: StockFilterType;
  onChange: (value: StockFilterType) => void;
}

export const StockFilter = ({ value, onChange }: StockFilterProps) => {
  return (
    <div className="stock-filter">
      <label htmlFor="stock-select" className="filter-label">Stock:</label>
      <select
        id="stock-select"
        value={value}
        onChange={(e) => onChange(e.target.value as StockFilterType)}
        className="stock-select"
      >
        <option value="all">All Items</option>
        <option value="in-stock">In Stock</option>
        <option value="out-of-stock">Out of Stock</option>
      </select>
    </div>
  );
};
