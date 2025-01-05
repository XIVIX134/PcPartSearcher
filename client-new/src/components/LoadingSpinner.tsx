import '@styles/LoadingSpinner.css';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  className?: string;
}

export const LoadingSpinner = ({ size = 'medium', className = '' }: LoadingSpinnerProps) => {
  return (
    <div className={`spinner-container ${className}`}>
      <div className={`spinner spinner-${size}`}>
        {Array.from({ length: 12 }).map((_, index) => (
          <div key={index} className="spinner-blade" />
        ))}
      </div>
    </div>
  );
};
