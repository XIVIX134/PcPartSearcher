import type { SourceType } from '../types';
import '../styles/SourceFilters.css';

interface SourceFiltersProps {
  filters: Record<SourceType, boolean>;
  onFilterChange: (source: SourceType) => void;
  availableSources?: SourceType[];
}

export const SourceFilters: React.FC<SourceFiltersProps> = ({
  filters,
  onFilterChange,
  availableSources
}) => {
  const sources = availableSources?.length ? availableSources : Object.keys(filters) as SourceType[];
  
  return (
    <div className="source-filters">
      {sources.map(source => (
        <label key={source} className="filter-option">
          <input
            type="checkbox"
            checked={filters[source]}
            onChange={() => onFilterChange(source)}
          />
          {source.toUpperCase()}
        </label>
      ))}
    </div>
  );
};
