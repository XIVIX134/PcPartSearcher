import { SourceFilters } from './SourceFilters';
import { StockFilter } from './StockFilter';
import { SortControls } from './SortControls';
import { ViewToggle } from './ViewToggle';
import type { SourceType, StockFilter as StockFilterType } from '../types';
import '../styles/FiltersBar.css';

interface FiltersBarProps {
  className?: string;
  sourceFilters: Record<SourceType, boolean>;
  stockFilter: StockFilterType;
  sortOption: 'price-asc' | 'price-desc' | 'newest';
  view: 'grid' | 'list';
  onSourceFilterChange: (source: SourceType) => void;
  onStockFilterChange: (value: StockFilterType) => void;
  onSortChange: (value: 'price-asc' | 'price-desc' | 'newest') => void;
  onViewChange: (view: 'grid' | 'list') => void;
  gridSize: number;
  onGridSizeChange: (size: number) => void;
}

export const FiltersBar = ({
  className = '',
  sourceFilters,
  stockFilter,
  sortOption,
  view,
  onSourceFilterChange,
  onStockFilterChange,
  onSortChange,
  onViewChange,
  gridSize,
  onGridSizeChange,
}: FiltersBarProps) => {
  const isMobile = window.innerWidth <= 768;

  return (
    <div className={`filters-bar ${className}`}>
      <div className="filters-group">
        <SourceFilters 
          filters={sourceFilters}
          onFilterChange={onSourceFilterChange}
        />
        <StockFilter 
          value={stockFilter}
          onChange={onStockFilterChange}
        />
      </div>
      <div className="filters-group">
        <SortControls
          onSort={onSortChange}
          currentSort={sortOption}
        />
        <ViewToggle 
          view={view}
          onViewChange={onViewChange}
        />
        {isMobile && (
          <div className="grid-size-control">
            <label htmlFor="gridSize">Cards per row: {gridSize}</label>
            <input
              type="range"
              id="gridSize"
              min="1"
              max="2"
              step="1"
              value={gridSize}
              onChange={(e) => onGridSizeChange(Number(e.target.value))}
              className="grid-size-slider"
            />
          </div>
        )}
      </div>
    </div>
  );
};
