import React, { useState } from 'react';
import { motion } from 'framer-motion';
import ButtonSelector from './ButtonSelector';
import ImageToggle from './ImageToggle';
import SearchButton from './SearchButton';
import UploadButton from './UploadButton';
import './ContentForm.css';

// Importar iconos de plataformas
import twitterIcon from '../../assets/images/twitter.svg';
import linkedinIcon from '../../assets/images/linkedin.svg';
import instagramIcon from '../../assets/images/instagram.svg';
import blogIcon from '../../assets/images/blog.svg';

const ContentForm = ({ onSubmit, loading }) => {  const [formData, setFormData] = useState({
    topic: '',
    platform: '',
    company: '',
    tone: '',
    language: '',
    audience: '',
    model_writer: '',
    model_research: '',
    generateImage: true,
    imageMode: '',
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  // Función para manejar contenido seleccionado desde SearchButton
  const handleContentSelect = (selectedContent) => {
    setFormData(prev => ({
      ...prev,
      topic: selectedContent
    }));
  };
  // Model selection is now handled directly by the ModelSelector component
  const handleImageModeChange = (mode) => {
    setFormData({
      ...formData,
      imageMode: mode
    });
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  // Opciones para los selectores
  const tones = ["profesional", "cercano", "informativo", "humorístico", "técnico", "inspirador", "motivacional", "formal", "casual", "persuasivo"];
  const languages = ["Español", "Inglés", "Francés", "Italiano"];
  const models = ["mistralai/mistral-7b-instruct", "meta-llama/llama-3-8b-instruct", "openai/gpt-3.5-turbo"];
  const platforms = [
    { name: 'Twitter', icon: twitterIcon },
    { name: 'Instagram', icon: instagramIcon },
    { name: 'LinkedIn', icon: linkedinIcon },
    { name: 'Blog', icon: blogIcon }
  ];

  return (
    <motion.div 
      className="form-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <form 
          onSubmit={handleSubmit} 
          className="content-form" 
          aria-labelledby="main-title" 
          aria-describedby="main-description"
        >
        <div className="form-grid two-cols" role="group">
          {/* Primera fila: Tema y Marca/Empresa */}
          <div className="form-group">
            <label htmlFor="topic" className="form-label">
              Tema del contenido
              <span className="tooltip-icon" data-tooltip-id="tooltip-component" data-tooltip-content="Define el tema principal sobre el que se generará el contenido">i</span>
            </label>
            <input
              type="text"
              id="topic"
              name="topic"
              value={formData.topic}
              onChange={handleChange}
              className="form-input"
              placeholder="Ej: Consejos para ingenieros, marketing digital, ideas para Instagram, etc."
              required
            />
            <div className="upload-below-input">
              <UploadButton />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="company" className="form-label">
              Marca o empresa
              <span className="tooltip-icon" data-tooltip-id="tooltip-component" data-tooltip-content="Nombre de tu empresa para personalizar el contenido">i</span>
            </label>
            <input
              type="text"
              id="company"
              name="company"
              value={formData.company}
              onChange={handleChange}
              className="form-input"
              placeholder="Ej: Círculo Creativo, Nike, Apple, etc."
            />
          </div>
          {/* Segunda fila: Idioma y Tono */}
          <div className="form-group">
            <label className="form-label">
              Idioma del contenido
              <span className="tooltip-icon" data-tooltip-id="tooltip-component" data-tooltip-content="Selecciona el idioma en el que se generará el contenido">i</span>
            </label>
            <ButtonSelector 
              options={languages}
              selected={formData.language}
              onChange={handleChange}
              name="language"
            />
          </div>
          <div className="form-group">
            <label className="form-label">
              Tono del mensaje
              <span className="tooltip-icon" data-tooltip-id="tooltip-component" data-tooltip-content="Define el estilo de comunicación del contenido">i</span>
            </label>
            <ButtonSelector 
              options={tones}
              selected={formData.tone}
              onChange={handleChange}
              name="tone"
            />
          </div>
        </div>
        {/* Tercera fila: Modelo y Audiencia en una sola columna */}
        <div className="form-grid one-col">
          <div className="form-group">
            <label className="form-label">
              Modelo LLM
              <span className="tooltip-icon" data-tooltip-id="tooltip-component" data-tooltip-content="Modelo de lenguaje a utilizar para la generación de contenido">i</span>
            </label>
            <ButtonSelector 
              options={models}
              selected={formData.model_writer}
              onChange={handleChange}
              name="model_writer"
            />
          </div>
          <div className="form-group">
            <label htmlFor="audience" className="form-label">
              Audiencia objetivo 
              <span className="tooltip-icon" data-tooltip-id="tooltip-component" data-tooltip-content="Describe el público al que va dirigido el contenido">i</span>
            </label>
            <input
              type="text"
              id="audience"
              name="audience"
              value={formData.audience}
              onChange={handleChange}
              className="form-input"
              placeholder="Ej: Profesionales de marketing, estudiantes, ingenieros, etc."
            />
          </div>
        </div>
        {/* Agrupa plataforma y generación de imagen en una fila visual */}
        <div className="platform-image-row">
          <div className="form-group platform-group">
            <label className="form-label">
              Plataforma
              <span className="tooltip-icon" data-tooltip-id="tooltip-component" data-tooltip-content="Selecciona la red social para la que se adaptará el contenido">i</span>
            </label>
            <ButtonSelector 
              options={platforms}
              selected={formData.platform}
              onChange={handleChange}
              name="platform"
            />
          </div>
          <div className="form-group image-generation-container">
            <ImageToggle
              isChecked={!!formData.generateImage}
              onChange={e => setFormData({
                ...formData,
                generateImage: e.target.checked
              })}
              onModeChange={handleImageModeChange}
            />
          </div>
        </div>
        {/* Componente de búsqueda de publicaciones */}
        <div className="search-section">
          <SearchButton onContentSelect={handleContentSelect} />
        </div>
        <button 
          type="submit" 
          className={`submit-button ${loading ? 'loading' : ''}`}
          disabled={loading}
          aria-live="polite"
        >
          <span className="visually-hidden">
            {loading ? 'Generando contenido, por favor espere' : 'Generar contenido con Magic Post'}
          </span>
          <span aria-hidden="true">
            {loading ? 'Generando...' : 'Generar contenido'}
          </span>
        </button>
      </form>
    </motion.div>
  );
};

export default ContentForm;