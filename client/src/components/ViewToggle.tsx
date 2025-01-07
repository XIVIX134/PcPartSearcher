import '@styles/ViewToggle.css';

interface ViewToggleProps {
  view: 'grid' | 'list';
  onViewChange: (view: 'grid' | 'list') => void;
}

export const ViewToggle = ({ view, onViewChange }: ViewToggleProps) => {
  return (
    <div className="view-toggle">
      <button
        className={`toggle-btn ${view === 'grid' ? 'active' : ''}`}
        onClick={() => onViewChange('grid')}
        aria-label="Grid view"
      >
        <GridIcon />
      </button>
      <button
        className={`toggle-btn ${view === 'list' ? 'active' : ''}`}
        onClick={() => onViewChange('list')}
        aria-label="List view"
      >
        <ListIcon />
      </button>
    </div>
  );
};

const GridIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <path d="M3 3h7v7H3V3zm11 0h7v7h-7V3zm0 11h7v7h-7v-7zM3 14h7v7H3v-7z" />
  </svg>
);

const ListIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <path d="M3 4h18v4H3V4zm0 6h18v4H3v-4zm0 6h18v4H3v-4z" />
  </svg>
);
