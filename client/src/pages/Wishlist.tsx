import { useState, useMemo } from 'react';
import { ProductCard } from '../components/ProductCard';
import { ViewToggle } from '../components/ViewToggle';
import { SortControls } from '../components/SortControls';
import { Toast } from '../components/Toast';
import type { Product } from '../types';
import { normalizePrice } from '../utils/productUtils';
import '../styles/Wishlist.css';

export const WishlistPage = () => {
  const [view, setView] = useState<'grid' | 'list'>('grid');
  const [sortOption, setSortOption] = useState<'price-asc' | 'price-desc' | 'newest'>('newest');
  // Placeholder wishlist data - will be replaced with backend data later
  const [wishlistItems] = useState<Product[]>([]);
  const [showRemoveConfirm, setShowRemoveConfirm] = useState(false);
  const [itemToRemove, setItemToRemove] = useState<Product | null>(null);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  const handleWishlistToggle = (product: Product) => {
    setItemToRemove(product);
    setShowRemoveConfirm(true);
  };

  const handleConfirmRemove = () => {
    // Will be implemented with backend
    setShowRemoveConfirm(false);
    setItemToRemove(null);
    setToast({
      message: 'Item removed from wishlist',
      type: 'success'
    });
  };

  const handleRemoveAll = () => {
    // Will be implemented with backend
    setToast({
      message: 'All items removed from wishlist',
      type: 'success'
    });
  };

  // Sort products based on selected option
  const sortedWishlistItems = useMemo(() => {
    if (sortOption === 'newest') {
      return [...wishlistItems].reverse(); // Assuming newest items are added last
    }

    return [...wishlistItems].sort((a, b) => {
      const priceA = normalizePrice(a.Price);
      const priceB = normalizePrice(b.Price);
      return sortOption === 'price-asc' ? priceA - priceB : priceB - priceA;
    });
  }, [wishlistItems, sortOption]);

  return (
    <div className="wishlist-page">
      <div className="wishlist-container">
        <div className="wishlist-header">
          <h1>My Wishlist</h1>
          {wishlistItems.length > 0 && (
            <div className="wishlist-controls">
              <ViewToggle view={view} onViewChange={setView} />
              <SortControls onSort={setSortOption} currentSort={sortOption} />
              <button 
                className="remove-all-button"
                onClick={handleRemoveAll}
                title="Remove all items"
              >
                Clear Wishlist
              </button>
            </div>
          )}
        </div>
        
        <div className="wishlist-content">
          {wishlistItems.length === 0 ? (
            <div className="empty-wishlist">
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2"
                className="empty-icon"
              >
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
              <p className="empty-title">Your wishlist is empty</p>
              <p className="empty-subtitle">Start adding products you like to keep track of them</p>
            </div>
          ) : (
            <div className={`wishlist-grid view-${view}`}>
              {sortedWishlistItems.map((product) => (
                <ProductCard 
                  key={product.uid} 
                  product={product}
                  showWishlistButton={true}
                  isInWishlist={true}
                  onWishlistToggle={handleWishlistToggle}
                />
              ))}
            </div>
          )}
        </div>

        {/* Remove Confirmation Modal */}
        {showRemoveConfirm && itemToRemove && (
          <div className="modal-overlay" onClick={() => setShowRemoveConfirm(false)}>
            <div className="confirm-modal" onClick={e => e.stopPropagation()}>
              <h3>Remove from Wishlist</h3>
              <p>Are you sure you want to remove this item from your wishlist?</p>
              <div className="modal-actions">
                <button 
                  className="cancel-button"
                  onClick={() => setShowRemoveConfirm(false)}
                >
                  Cancel
                </button>
                <button 
                  className="confirm-button"
                  onClick={handleConfirmRemove}
                >
                  Remove
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Toast Notifications */}
        {toast && (
          <Toast
            message={toast.message}
            type={toast.type}
            onClose={() => setToast(null)}
          />
        )}
      </div>
    </div>
  );
};