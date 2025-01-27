import { Link, useLocation } from 'react-router-dom';
import '../styles/Header.css';

export const Header = () => {
  const location = useLocation();
  const isHomePage = location.pathname === '/';

  return (
    <header className="header">
      {!isHomePage && (
        <Link to="/" className="title-link">
          <h1 className="title-glow">PC Part Searcher</h1>
        </Link>
      )}
    </header>
  );
};