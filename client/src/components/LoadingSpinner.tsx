import { useEffect, useRef, useState, useCallback } from 'react';
import '@styles/LoadingSpinner.css';

const LOADING_TEXT = 'SEARCHING';
const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+{}|[]\\;\':"<>?,./`~'.split('');

interface TickerLetter {
  original: string;  // Like 'data-orig'
  current: string;   // Displayed character
  done: boolean;     // Matches .done class
}

interface LoadingSpinnerProps {
  className?: string;
  onReset?: () => void;
  autoReset?: boolean;
  size?: 'small' | 'medium' | 'large';  // Add size prop
}

export const LoadingSpinner = ({ className = '', onReset, autoReset = false }: LoadingSpinnerProps) => {
  // Initialize letters with each letter's 'original' and a placeholder
  const [letters, setLetters] = useState<TickerLetter[]>(
    () => LOADING_TEXT.split('').map(ch => ({
      original: ch,
      current: '-',
      done: false
    }))
  );

  // Mirrors Ticker fields
  const cycleCount = useRef(2); // Changed from 5 to 2 for shorter scramble duration
  const cycleCurrent = useRef(0);
  const charsCount = CHARS.length;
  const letterCount = LOADING_TEXT.length;
  const letterCurrent = useRef(0);
  const doneRef = useRef(false);
  const frameRef = useRef<number>();

  // Translates Ticker.prototype.getChar
  const getChar = useCallback(() => {
    return CHARS[Math.floor(Math.random() * charsCount)];
  }, [charsCount]);

  // Translates Ticker.prototype.loop
  const loop = useCallback(() => {
    setLetters(prev => {
      const updated = [...prev];
      
      // Add delay between frames to slow down scrambling
      const now = Date.now();
      if (now - (frameRef.current || 0) < 50) { // 50ms delay between updates
        return prev;
      }
      frameRef.current = now;

      // Update random characters
      updated.forEach((letter, index) => {
        if (index >= letterCurrent.current && letter.original !== ' ') {
          updated[index] = {
            ...letter,
            current: getChar(),
          };
        }
      });

      if (cycleCurrent.current < cycleCount.current) {
        cycleCurrent.current++;
      } else if (letterCurrent.current < letterCount) {
        const idx = letterCurrent.current;
        updated[idx] = {
          ...updated[idx],
          current: updated[idx].original,
          done: true
        };
        cycleCurrent.current = 0;
        letterCurrent.current++;
      } else {
        // When complete, wait before starting a new cycle
        setTimeout(() => {
          letterCurrent.current = 0;
          cycleCurrent.current = 0;
          setLetters(prev => prev.map(letter => ({
            ...letter,
            done: false
          })));
        }, 1500); // 1.5 second pause when complete
        return prev; // Keep showing SEARCHING during pause
      }

      return updated;
    });

    frameRef.current = requestAnimationFrame(loop);
  }, [getChar, letterCount]);

  // Translates Ticker.prototype.reset
  const resetTicker = useCallback(() => {
    doneRef.current = false;
    cycleCurrent.current = 0;
    letterCurrent.current = 0;
    setLetters(prev => prev.map(letter => ({
      ...letter,
      current: letter.original, // Reset to original text visually
      done: false
    })));
    // Then replace them all with '-' to restart just like jQuery
    // in the next tick, so it toggles again as in the original code
    setTimeout(() => {
      setLetters(prev => prev.map(letter => ({
        ...letter,
        current: letter.original === ' ' ? ' ' : '-',
        done: false
      })));
      requestAnimationFrame(loop); // Kick off again
    }, 0);
  }, [loop]);

  // On mount, just start the loop
  useEffect(() => {
    frameRef.current = requestAnimationFrame(loop);
    if (onReset) {
      onReset();
    }
    if (autoReset) {
      resetTicker();
    }
    return () => {
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current);
      }
    };
  }, [onReset, autoReset, loop, resetTicker]);

  return (
    <div className={`loader-wrapper ${className}`}>
      <div className="word">
        {letters.map((letter, i) => (
          <span
            key={i}
            className={letter.done ? 'done' : ''}
          >
            {letter.current}
          </span>
        ))}
        <div className="overlay" />
      </div>
    </div>
  );
};
