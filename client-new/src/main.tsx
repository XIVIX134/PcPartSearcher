import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles/global.css'

// Create root only once
let root: ReturnType<typeof createRoot> | null = null;

// Position interface
interface Position {
  x: number;
  y: number;
}

// Blob animation hook
export const useBlobAnimation = () => {
  const [position, setPosition] = React.useState<Position>({ 
    x: window.innerWidth / 2, 
    y: window.innerHeight / 2 
  });
  
  const mousePos = React.useRef<Position>(position);
  const frameRef = React.useRef<number>();

  const animate = React.useCallback(() => {
    setPosition({
      x: mousePos.current.x,
      y: mousePos.current.y
    });
    frameRef.current = requestAnimationFrame(animate);
  }, []);

  React.useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      // Update mousePos directly without state
      mousePos.current = { x: e.clientX, y: e.clientY };
    };

    window.addEventListener('mousemove', handleMouseMove);
    frameRef.current = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current);
      }
    };
  }, [animate]);

  return mousePos.current; // Return ref value directly
};

// Initialize app only if not already initialized
if (!root) {
  const container = document.getElementById('root');
  if (container) {
    root = createRoot(container);
    root.render(<App />);
  }
}

export type { Position };
