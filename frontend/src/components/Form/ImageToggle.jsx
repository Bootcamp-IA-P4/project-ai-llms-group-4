import React from 'react';
import './ImageToggle.css';
import imageIcon from '../../assets/images/image-icon.svg';

const ImageToggle = ({ isChecked, onChange, onModeChange, onImageDetailsChange }) => {
  const [imageGenMode, setImageGenMode] = React.useState('automatic');  const [imageDetails, setImageDetails] = React.useState({
    subject: '',
    style: '',
    medium: '',
    lighting: '',
    color: '',
    composition: '',
    resolution: '',
    contrast: '',
    mood: '',
    details: ''
  });

  // Opciones para cada campo
  const styleOptions = ["Fotográfico", "Ilustración", "3D", "Dibujos animados", "Realista", "Abstracto"];
  const mediumOptions = ["Digital", "Óleo", "Acuarela", "Lápiz", "Fotografía"];
  const lightingOptions = ["Natural", "Dramática", "Suave", "Dura", "Hora dorada", "Neón"];
  const colorOptions = ["Vibrante", "Pastel", "Monocromático", "Cálidos", "Fríos", "Tierra"];
  const compositionOptions = ["Centrado", "Regla de tercios", "Diagonal", "Simétrico", "Primer plano", "Plano general"];
  const resolutionOptions = ["1024x1024 (Cuadrado)", "1024x768 (Horizontal)", "768x1024 (Vertical)", "1280x720 (HD)"];
  const contrastOptions = ["Alto", "Medio", "Bajo", "Suave"];
  const moodOptions = ["Alegre", "Misterioso", "Tranquilo", "Enérgico", "Romántico", "Profesional"];

  // Componente helper para grupos de botones
  const ButtonGroup = ({ label, options, value, onChange, field }) => (
    <div className="image-field">
      <label className="image-field-label">{label}</label>
      <div className="image-button-group">
        {options.map((option) => (
          <button
            key={option}
            type="button"
            className={`image-option-btn ${value === option ? 'active' : ''}`}
            onClick={() => onChange(field, option)}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );

  const handleModeChange = (mode) => {
    setImageGenMode(mode);
    if (onModeChange) {
      onModeChange(mode);
    }
  };

  const handleImageDetailChange = (field, value) => {
    const updatedDetails = { ...imageDetails, [field]: value };
    setImageDetails(updatedDetails);
    if (onImageDetailsChange) {
      onImageDetailsChange(updatedDetails);
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
        <div className="image-options">          <div className="image-mode-selector">
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

          {imageGenMode === 'manual' && (
            <div className="manual-image-controls">              <div className="image-fields-grid">
                <div className="image-field">
                  <label className="image-field-label">Sujeto</label>
                  <input
                    type="text"
                    value={imageDetails.subject}
                    onChange={(e) => handleImageDetailChange('subject', e.target.value)}
                    placeholder="Ej: Una persona, un paisaje..."
                    className="image-text-input"
                  />
                </div>

                <ButtonGroup 
                  label="Estilo" 
                  options={styleOptions} 
                  value={imageDetails.style} 
                  onChange={handleImageDetailChange} 
                  field="style" 
                />

                <ButtonGroup 
                  label="Medio" 
                  options={mediumOptions} 
                  value={imageDetails.medium} 
                  onChange={handleImageDetailChange} 
                  field="medium" 
                />

                <ButtonGroup 
                  label="Iluminación" 
                  options={lightingOptions} 
                  value={imageDetails.lighting} 
                  onChange={handleImageDetailChange} 
                  field="lighting" 
                />

                <ButtonGroup 
                  label="Paleta de Colores" 
                  options={colorOptions} 
                  value={imageDetails.color} 
                  onChange={handleImageDetailChange} 
                  field="color" 
                />

                <ButtonGroup 
                  label="Composición" 
                  options={compositionOptions} 
                  value={imageDetails.composition} 
                  onChange={handleImageDetailChange} 
                  field="composition" 
                />

                <ButtonGroup 
                  label="Resolución" 
                  options={resolutionOptions} 
                  value={imageDetails.resolution} 
                  onChange={handleImageDetailChange} 
                  field="resolution" 
                />

                <ButtonGroup 
                  label="Contraste" 
                  options={contrastOptions} 
                  value={imageDetails.contrast} 
                  onChange={handleImageDetailChange} 
                  field="contrast" 
                />

                <ButtonGroup 
                  label="Ambiente" 
                  options={moodOptions} 
                  value={imageDetails.mood} 
                  onChange={handleImageDetailChange} 
                  field="mood" 
                />

                <div className="image-field full-width">
                  <label className="image-field-label">Detalles</label>
                  <textarea
                    value={imageDetails.details}
                    onChange={(e) => handleImageDetailChange('details', e.target.value)}
                    placeholder="Detalles adicionales para la imagen..."
                    rows="3"
                    className="image-textarea"
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ImageToggle;