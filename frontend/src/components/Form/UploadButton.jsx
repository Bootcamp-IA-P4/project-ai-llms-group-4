import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { uploadDocument } from '../../api';
import './UploadButton.css';
import RainbowUploadIcon from '../../assets/images/image-icon.svg'; // Usa un SVG bonito si tienes, si no, reemplaza por un emoji o icono

const UploadButton = () => {
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validar tipo de archivo (solo texto)
      if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
        setUploadFile(file);
        setUploadMessage('');
      } else {
        setUploadMessage('❌ Solo se permiten archivos de texto (.txt)');
        setUploadFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!uploadFile) return;

    setUploadLoading(true);
    setUploadMessage('');

    try {
      const result = await uploadDocument(uploadFile);
      setUploadMessage('✅ Documento subido exitosamente');
      
      // Agregar archivo a la lista de subidos
      setUploadedFiles(prev => [...prev, uploadFile.name]);
      
      setUploadFile(null);
      // Reset file input
      const fileInput = document.getElementById('document-upload');
      if (fileInput) fileInput.value = '';
      
      // Auto collapse after 3 seconds
      setTimeout(() => {
        setIsExpanded(false);
        setUploadMessage('');
      }, 3000);
    } catch (error) {
      console.error('Error subiendo documento:', error);
      setUploadMessage('❌ Error al subir el documento');
    } finally {
      setUploadLoading(false);
    }
  };

  return (
    <div className="upload-button-container">
      {/* Overlay modal para el panel de subida */}
      {isExpanded && <div className="upload-modal-overlay" onClick={() => setIsExpanded(false)} />}
      <button
        type="button"
        className={`upload-toggle-btn rainbow-btn ${isExpanded ? 'active' : ''}`}
        onClick={() => setIsExpanded(!isExpanded)}
        disabled={uploadLoading}
      >
        <img src={RainbowUploadIcon} alt="Subir" className="upload-icon-svg" />
        <span className="upload-text">Subir Documento</span>
        {uploadLoading && <span className="loading-spinner">⏳</span>}
      </button>

      {uploadedFiles.length > 0 && (
        <div className="uploaded-files-list">
          <h5>Documentos subidos:</h5>
          {uploadedFiles.map((fileName, index) => (
            <div key={index} className="uploaded-file-item">
              📄 {fileName}
            </div>
          ))}
        </div>
      )}

      {isExpanded && (
        <div className="upload-modal-centered">
          <motion.div 
            className="upload-panel-modal"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            <div className="upload-header">
              <h4>📤 Subir Documento</h4>
              <button 
                className="close-upload"
                onClick={() => setIsExpanded(false)}
                aria-label="Cerrar"
              >
                ×
              </button>
            </div>
            <div className="upload-form">
              <div className="upload-input-group">
                <input
                  type="file"
                  id="document-upload"
                  accept=".txt"
                  onChange={handleFileChange}
                  className="upload-input"
                  disabled={uploadLoading}
                />
                <label htmlFor="document-upload" className={`upload-label ${uploadFile ? 'selected' : ''}`}>
                  {uploadFile ? `📄 ${uploadFile.name}` : '📄 Seleccionar archivo .txt'}
                </label>
                {uploadFile && (
                  <button 
                    type="button" 
                    className="submit-upload-btn rainbow-btn"
                    disabled={uploadLoading}
                    onClick={handleUpload}
                  >
                    {uploadLoading ? '⏳ Subiendo...' : '📤 Subir'}
                  </button>
                )}
              </div>
            </div>
            {uploadMessage && (
              <div className={`upload-message ${uploadMessage.includes('✅') ? 'success' : 'error'}`}>
                {uploadMessage}
              </div>
            )}
            <small className="upload-help">
              💡 Los documentos de texto mejoran las búsquedas semánticas
            </small>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default UploadButton;