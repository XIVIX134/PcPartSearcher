import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SearchPage } from './pages/Search';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SearchPage />} />
      </Routes>
    </BrowserRouter>
  );
};
