import { useEffect } from 'react';
import { SourceFilters } from './SourceFilters';
import type { SourceType } from '../types';
import { setCookie } from '../utils/cookies';
import '../styles/AdvancedSearchModal.css';

interface AdvancedSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  sourceFilters: Record<SourceType, boolean>;
  onSourceFilterChange: (source: SourceType) => void;
  onSearch: () => void;
}

export const AdvancedSearchModal = ({
  isOpen,
  onClose,
  sourceFilters,
  onSourceFilterChange,
  onSearch
}: AdvancedSearchModalProps) => {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  const handleSave = () => {
    // Save preferences to cookies
    setCookie('searchPreferences', {
      sourceFilters
    });
    onClose(); // Close first
    setTimeout(() => {
      onSearch(); // Then trigger search after a small delay
    }, 50);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>×</button>
        <h2>Advanced Search Settings</h2>
        <div className="modal-body">
          <div className="settings-group">
            <h3>Select Sources</h3>
            <p>Choose which websites to include in your search:</p>
            <SourceFilters 
              filters={sourceFilters}
              onFilterChange={onSourceFilterChange}
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
