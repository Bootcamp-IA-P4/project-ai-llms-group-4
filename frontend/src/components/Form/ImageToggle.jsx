import React from 'react';
import './ImageToggle.css';
import imageIcon from '../../assets/images/image-icon.svg';

const ImageToggle = ({ isChecked, onChange, onModeChange }) => {
  const [imageGenMode, setImageGenMode] = React.useState('automatic');

  const handleModeChange = (mode) => {
    setImageGenMode(mode);
    if (onModeChange) {
      onModeChange(mode);
    }
  };

  return (
    <div className="image-toggle-container">
      <div className="toggle-header">
        <label className="toggle-switch" htmlFor="image-toggle">
          <input
            type="checkbox"
            id="image-toggle"
            checked={isChecked}
            onChange={onChange}
            aria-labelledby="toggle-label"
          />
          <span className="toggle-slider">
            <span className="toggle-on">ON</span>
            <span className="toggle-off">OFF</span>
          </span>
        </label>
        <span className="toggle-label" id="toggle-label">
          <img src={imageIcon} alt="" className="toggle-icon" aria-hidden="true" />
          Generar imagen con IA
        </span>
      </div>
      
      {isChecked && (
        <div className="image-options">
          <div className="image-mode-selector">
            <button 
              type="button"
              className={`image-mode-btn ${imageGenMode === 'automatic' ? 'active' : ''}`}
              onClick={() => handleModeChange('automatic')}
            >
              Automático
            </button>
            <button 
              type="button"
              className={`image-mode-btn ${imageGenMode === 'manual' ? 'active' : ''}`}
              onClick={() => handleModeChange('manual')}
            >
              Manual
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageToggle;