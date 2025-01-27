import { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/UserMenu.css';

export const UserMenu = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="user-menu">
      <button 
        className="profile-button" 
        onClick={() => setIsOpen(!isOpen)}
        aria-label="User menu"
      >
        <div className="profile-circle">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2"
          >
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        </div>
      </button>
      {isOpen && (
        <div className="dropdown-menu">
          <Link to="/" className="menu-item" onClick={() => setIsOpen(false)}>
            Home
          </Link>
          <div className="menu-divider"></div>
          <Link to="/account" className="menu-item" onClick={() => setIsOpen(false)}>
            Account
          </Link>
          <Link to="/wishlist" className="menu-item" onClick={() => setIsOpen(false)}>
            Wishlist
          </Link>
        </div>
      )}
    </div>
  );
};