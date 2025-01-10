import { useEffect, useState } from 'react';
import { SourceFilters } from './SourceFilters';
import type { SourceType } from '../types';
import { setCookie } from '../utils/cookies';
import '../styles/AdvancedSearchModal.css';

interface AdvancedSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  sourceFilters: Record<SourceType, boolean>;
  onSourceFilterChange: (filters: Record<SourceType, boolean>) => void;
  onSearch: () => void;
  searchTerm?: string;
  lastSearchTerm: string;
  searchedSources: Record<SourceType, boolean>;
}

export const AdvancedSearchModal = ({
  isOpen,
  onClose,
  sourceFilters,
  onSourceFilterChange,
}: AdvancedSearchModalProps) => {
  const [tempFilters, setTempFilters] = useState(sourceFilters);

  useEffect(() => {
    if (isOpen) {
      setTempFilters(sourceFilters);
    }
  }, [isOpen, sourceFilters]);

  const handleFilterChange = (source: SourceType) => {
    const isCurrentlyEnabled = tempFilters[source];
    
    // Check if this would be the last enabled source
    const otherSourcesEnabled = Object.entries(tempFilters)
      .filter(([key]) => key !== source)
      .some(([, enabled]) => enabled);

    // Don't allow unchecking if it's the last enabled source
    if (isCurrentlyEnabled && !otherSourcesEnabled) {
      return;
    }

    setTempFilters(prev => ({
      ...prev,
      [source]: !prev[source]
    }));
  };

  const handleSave = () => {
    // Check if at least one source is selected
    const hasSelectedSource = Object.values(tempFilters).some(Boolean);
    if (!hasSelectedSource) {
      // If no sources are selected, select the first one by default
      const firstSource = Object.keys(tempFilters)[0] as SourceType;
      const updatedFilters = {
        ...tempFilters,
        [firstSource]: true
      };
      setTempFilters(updatedFilters);
      onSourceFilterChange(updatedFilters);
      onClose();
      return;
    }

    onSourceFilterChange(tempFilters);
    setCookie('searchPreferences', { sourceFilters: tempFilters });
    onClose();
  };

  return (
    <div className={`modal-overlay ${isOpen ? 'visible' : ''}`} onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <h2>Advanced Search Settings</h2>
        <div className="modal-body">
          <div className="settings-group">
            <h3>Select Sources</h3>
            <p>Choose which websites to include in your search:</p>
            <SourceFilters 
              filters={tempFilters}
              onFilterChange={handleFilterChange}
            />
          </div>
          <div className="modal-footer">
            <button className="modal-button cancel" onClick={onClose}>
              Cancel
            </button>
            <button className="modal-button search" onClick={handleSave}>
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
