import type { SourceType, SourceFilters as SourceFiltersType } from '../types';
import '../styles/SourceFilters.css';

interface SourceFiltersProps {
  filters: SourceFiltersType;
  onFilterChange: (source: SourceType) => void;
}

export const SourceFilters = ({ filters, onFilterChange }: SourceFiltersProps) => {
  return (
    <div className="source-filters">
      <span className="filter-label">Search in:</span>
      {(Object.keys(filters) as SourceType[]).map((source) => (
        <label key={source} className="filter-option">
          <input
            type="checkbox"
            checked={filters[source]}
            onChange={() => onFilterChange(source)}
          />
          <span className="filter-text">{source.toUpperCase()}</span>
        </label>
      ))}
    </div>
  );
};
