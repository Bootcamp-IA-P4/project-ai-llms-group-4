import React, { useState } from 'react';
import { motion } from 'framer-motion';
import ButtonSelector from './ButtonSelector';
import ImageToggle from './ImageToggle';
import './ContentForm.css';

// Importar iconos de plataformas
import twitterIcon from '../../assets/images/twitter.svg';
import linkedinIcon from '../../assets/images/linkedin.svg';
import instagramIcon from '../../assets/images/instagram.svg';
import blogIcon from '../../assets/images/blog.svg';

const ContentForm = ({ onSubmit, loading }) => {  const [formData, setFormData] = useState({
    topic: 'Inteligencia Artificial',
    platform: 'Twitter',
    company: '',
    tone: 'Profesional',
    language: 'Español',
    audience: '',
    model: 'meta-llama/llama-3-8b-instruct',
    generateImage: true,
    imageMode: 'automatic',
    imageSize: '1024x1024',
    imageStyle: 'photographic',
    imagePrompt: '',
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
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
  };  // Opciones para los selectores
  // Nota: Estos arrays son manejados directamente por sus componentes respectivos
  const tones = ["Profesional", "Cercano", "Informativo", "Humorístico", "Técnico", "Inspirador", "Motivacional", "Formal", "Casual", "Persuasivo"];
  const languages = ["Español", "Inglés", "Francés", "Italiano", "Portugués", "Alemán"];
  const models = ["meta-llama/llama-3-8b-instruct", "gpt-3.5-turbo", "claude-3-haiku", "mistral-7b-instruct"];
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
      <h2 className="form-title" id="form-title" data-text="MAGIC POST Generator">MAGIC POST Generator</h2>
      <p className="form-description" id="form-description">
        Configura los parámetros para generar contenido optimizado para tu audiencia y plataforma
      </p>
      
      <form 
          onSubmit={handleSubmit} 
          className="content-form" 
          aria-labelledby="form-title" 
          aria-describedby="form-description"
        >        <div className="form-grid" role="group">
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
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="company" className="form-label">
              Marca o empresa (opcional)
              <span className="tooltip-icon" data-tooltip-id="tooltip-component" data-tooltip-content="Nombre de tu empresa para personalizar el contenido">i</span>
            </label>
            <input
              type="text"
              id="company"
              name="company"
              value={formData.company}
              onChange={handleChange}
              className="form-input"
              placeholder="Nombre de tu empresa"
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
          </div>          {/* Tercera fila: Modelo y Audiencia */}
          <div className="form-group">
            <label className="form-label">
              Modelo LLM
              <span className="tooltip-icon" data-tooltip-id="tooltip-component" data-tooltip-content="Modelo de lenguaje a utilizar para la generación de contenido">i</span>
            </label>
            <ButtonSelector 
              options={models}
              selected={formData.model}
              onChange={handleChange}
              name="model"
            />
          </div>
          <div className="form-group">
            <label htmlFor="audience" className="form-label">
              Audiencia objetivo (opcional)
              <span className="tooltip-icon" data-tooltip-id="tooltip-component" data-tooltip-content="Describe el público al que va dirigido el contenido">i</span>
            </label>
            <input
              type="text"
              id="audience"
              name="audience"
              value={formData.audience}
              onChange={handleChange}
              className="form-input"
              placeholder="Ej: Profesionales de marketing, estudiantes, etc."
            />
          </div>
        </div>
          {/* Plataforma en su propia fila */}
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
            isChecked={formData.generateImage}
            onChange={(e) => handleChange({
              target: {
                name: 'generateImage',
                type: 'checkbox',
                checked: e.target.checked
              }
            })}
            onModeChange={handleImageModeChange}          />
          
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
