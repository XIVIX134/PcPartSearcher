import '@styles/SortControls.css';

type SortOption = 'price-asc' | 'price-desc' | 'newest';

interface SortControlsProps {
  onSort: (option: SortOption) => void;
  currentSort: SortOption;
}

export const SortControls = ({ onSort, currentSort }: SortControlsProps) => {
  return (
    <div className="sort-controls">
      <label htmlFor="sort-select" className="sort-label">Sort by:</label>
      <select 
        id="sort-select"
        value={currentSort}
        onChange={(e) => onSort(e.target.value as SortOption)}
        className="sort-select"
      >
        <option value="newest">Newest First</option>
        <option value="price-asc">Price: Low to High</option>
        <option value="price-desc">Price: High to Low</option>
      </select>
    </div>
  );
};
