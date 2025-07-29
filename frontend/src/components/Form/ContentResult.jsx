import React from 'react';
import { motion } from 'framer-motion';
import './ContentResult.css';

const ContentResult = ({ content, prompt, imageUrl }) => {
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Contenido copiado al portapapeles');
  };

  return (
    <motion.div 
      className="result-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <h2 className="result-title" data-text="Contenido Generado">Contenido Generado</h2>
      
      <div className="result-section">
        <div className="result-header">
          <h3>Contenido</h3>
          <button 
            className="copy-button" 
            onClick={() => copyToClipboard(content)}
            data-tooltip-id="tooltip-component" 
            data-tooltip-content="Copiar al portapapeles"
          >
            Copiar
          </button>
        </div>
        <div className="content-display">
          {content.split('\n').map((paragraph, index) => (
            paragraph ? <p key={index}>{paragraph}</p> : <br key={index} />
          ))}
        </div>
      </div>

      {imageUrl && (
        <div className="result-section">
          <h3>Imagen generada</h3>
          <div className="image-container">
            <img src={imageUrl} alt="Imagen generada con IA" className="generated-image" />
            <a href={imageUrl} download="ai-generated-image.jpg" className="download-button">
              Descargar imagen
            </a>
          </div>
        </div>
      )}

     
      <div className="action-buttons">
        <button className="action-button share-button">
          Compartir resultados
        </button>
        <button className="action-button new-gen-button">
          Nueva generación
        </button>
      </div>
    </motion.div>
  );
};

export default ContentResult;
