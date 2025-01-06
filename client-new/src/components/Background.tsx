import { useBlobAnimation } from '../main';
import { useEffect, useState } from 'react';
import '../styles/Background.css';

export const Background = () => {
  const position = useBlobAnimation();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    return () => setMounted(false);
  }, []);

  if (!mounted) return null;

  const blobTransform = {
    x: (position.x - window.innerWidth/2) * 0.05,
    y: (position.y - window.innerHeight/2) * 0.05
  };

  return (
    <div className="background-wrapper">
      <div className="background-container">
        {/* Blur layer */}
        <div className="blur-layer">
          <div className="blur-content" />
        </div>

        {/* Content layers */}
        <div className="blob-container">
          <svg 
            viewBox="0 0 585 475" 
            className="blob"
            style={{
              transform: `translate(${blobTransform.x}px, ${blobTransform.y}px)`,
            }}
          >
            <path 
              className="blob-path"
              d="M59.6878 70.4072C2.64247 112.7 -16.8108 220.14 15.7866 303.15C34.714 338.439 85.6079 417.473 137.764 451.308C202.958 493.601 346.492 482.305 380.666 392.728C414.841 303.151 608.848 251.138 582.56 142.122C556.271 33.1053 429.562 31.2664 323.621 6.83623C217.68 -17.5939 116.733 28.1141 59.6878 70.4072Z"
            />
          </svg>
        </div>

        <div className="circle-container">
          <svg 
            width="100" 
            height="100" 
            viewBox="0 0 150 150"
            className="circle"
            style={{
              transform: `translate(${position.x - 50}px, ${position.y - 50}px)`,
            }}
          >
            <circle cx="75" cy="75" r="75" fill="#ffffff" />
          </svg>
        </div>
      </div>
    </div>
  );
};
