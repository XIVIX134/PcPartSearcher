import { useState, useEffect } from 'react';
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
  onSourceFilterChange: (filters: Record<SourceType, boolean>) => void; // Updated type
  onStockFilterChange: (value: StockFilterType) => void;
  onSortChange: (value: 'price-asc' | 'price-desc' | 'newest') => void;
  onViewChange: (view: 'grid' | 'list') => void;
  gridSize: number;
  onGridSizeChange: (size: number) => void;
  searchedSources: Record<SourceType, boolean>;
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
  searchedSources,
}: FiltersBarProps) => {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Show sources filter if there are any searched sources (not just enabled ones)
  const searchedSourcesList = Object.entries(searchedSources)
    .filter(([, searched]) => searched)
    .map(([source]) => source as SourceType);

  return (
    <div className={`filters-bar ${className}`}>
      {searchedSourcesList.length > 1 && (  // Changed condition to use searchedSources
        <div className="filter-section">
          <h3>Sources</h3>
          <SourceFilters 
            filters={sourceFilters}
            onFilterChange={(source: SourceType) => {
              onSourceFilterChange({
                ...sourceFilters,
                [source]: !sourceFilters[source]
              });
            }}
            availableSources={searchedSourcesList}  // Pass searched sources
          />
        </div>
      )}
      <div className="filters-group">
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
