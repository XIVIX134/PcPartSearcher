import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SearchPage } from './pages/Search';
import { AccountPage } from './pages/Account';
import { WishlistPage } from './pages/Wishlist';
import { Background } from './components/Background';
import { ErrorBoundary } from './components/ErrorBoundary';
import { UserMenu } from './components/UserMenu';
import { Header } from './components/Header';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

export default function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Background />
          <Header />
          <UserMenu />
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/account" element={<AccountPage />} />
            <Route path="/wishlist" element={<WishlistPage />} />
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}
