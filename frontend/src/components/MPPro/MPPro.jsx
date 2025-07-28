import React, { useState } from 'react';
import './MPPro.css';

const MPPro = () => {
  const [loading, setLoading] = useState(false);
  const [scientificData, setScientificData] = useState(null);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    topic: '',
    complexity: 'medium',
    targetAudience: 'general',
    articleType: 'research',
    includeImages: true,
    language: 'es'
  });

  const complexityLevels = [
    { value: 'basic', label: 'Básico', description: 'Para público general sin conocimientos técnicos' },
    { value: 'medium', label: 'Intermedio', description: 'Para lectores con conocimientos básicos' },
    { value: 'advanced', label: 'Avanzado', description: 'Para audiencia especializada' }
  ];
  const targetAudiences = [
    { value: 'general', label: 'Público General', icon: '' },
    { value: 'students', label: 'Estudiantes', icon: '' },
    { value: 'professionals', label: 'Profesionales', icon: '' },
    { value: 'researchers', label: 'Investigadores', icon: '' }
  ];

  const articleTypes = [
    { value: 'research', label: 'Investigación', description: 'Basado en papers científicos recientes' },
    { value: 'review', label: 'Revisión', description: 'Análisis de múltiples estudios' },
    { value: 'breakthrough', label: 'Descubrimiento', description: 'Últimos avances científicos' },
    { value: 'explainer', label: 'Explicativo', description: 'Conceptos científicos complejos simplificados' }
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Aquí se conectará con la API de revistas científicas
      // Por ahora simulamos una respuesta
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      setScientificData({
        title: `Contenido Científico sobre ${formData.topic}`,
        content: "Contenido generado basado en las últimas investigaciones científicas...",
        sources: [
          "Nature - Vol. 123, 2024",
          "Science - Vol. 456, 2024",
          "Cell - Vol. 789, 2024"
        ]
      });
    } catch (err) {
      setError('Error al generar contenido científico. Por favor intente nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mp-pro-container">
      <div className="mp-pro-content">        <header className="mp-pro-header">
          <h1 className="mp-pro-title" data-text="MAGIC POST PRO">
            <span className="visually-hidden">MAGIC POST PRO - Generador de Contenidos Científicos con IA</span>
            <span aria-hidden="true">MAGIC POST PRO</span>
          </h1>
          <p className="mp-pro-subtitle">
            Generación de contenido científico divulgativo basado en las últimas investigaciones
          </p>
        </header>

        <form onSubmit={handleSubmit} className="mp-pro-form">
          {/* Tema de investigación */}          <div className="form-section">
            <label className="form-label">
              <span className="label-text">Tema de Investigación</span>
            </label>
            <input
              type="text"
              name="topic"
              value={formData.topic}
              onChange={handleInputChange}
              placeholder="Ej: Inteligencia Artificial en medicina, CRISPR, Cambio climático..."
              className="form-input large"
              required
            />
          </div>

          {/* Nivel de Complejidad */}          <div className="form-section">
            <label className="form-label">
              <span className="label-text">Nivel de Complejidad</span>
            </label>
            <div className="complexity-grid">
              {complexityLevels.map((level) => (
                <div key={level.value} className="complexity-card">
                  <input
                    type="radio"
                    name="complexity"
                    value={level.value}
                    checked={formData.complexity === level.value}
                    onChange={handleInputChange}
                    className="complexity-radio"
                    id={`complexity-${level.value}`}
                  />
                  <label htmlFor={`complexity-${level.value}`} className="complexity-label">
                    <div className="complexity-title">{level.label}</div>
                    <div className="complexity-description">{level.description}</div>
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Audiencia Objetivo */}
          <div className="form-section">            <label className="form-label">
              <span className="label-text">Audiencia Objetivo</span>
            </label>
            <div className="audience-grid">
              {targetAudiences.map((audience) => (
                <div key={audience.value} className="audience-card">
                  <input
                    type="radio"
                    name="targetAudience"
                    value={audience.value}
                    checked={formData.targetAudience === audience.value}
                    onChange={handleInputChange}
                    className="audience-radio"
                    id={`audience-${audience.value}`}
                  />
                  <label htmlFor={`audience-${audience.value}`} className="audience-label">
                    <span className="audience-icon">{audience.icon}</span>
                    <span className="audience-text">{audience.label}</span>
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Tipo de Artículo */}
          <div className="form-section">            <label className="form-label">
              <span className="label-text">Tipo de Artículo</span>
            </label>
            <div className="article-grid">
              {articleTypes.map((type) => (
                <div key={type.value} className="article-card">
                  <input
                    type="radio"
                    name="articleType"
                    value={type.value}
                    checked={formData.articleType === type.value}
                    onChange={handleInputChange}
                    className="article-radio"
                    id={`article-${type.value}`}
                  />
                  <label htmlFor={`article-${type.value}`} className="article-label">
                    <div className="article-title">{type.label}</div>
                    <div className="article-description">{type.description}</div>
                  </label>
                </div>
              ))}
            </div>
          </div>          {/* Opciones adicionales */}
          <div className="form-section">
            <label className="form-label">
              <span className="label-text">Opciones Adicionales</span>
            </label>
            <div className="options-grid">
              <div className="option-card">
                <div className="toggle-section">
                  <span className="toggle-label">Incluir imágenes científicas</span>
                  <label className="toggle-switch">
                    <input
                      type="checkbox"
                      name="includeImages"
                      checked={formData.includeImages}
                      onChange={handleInputChange}
                      className="toggle-input"
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>
              </div>
              
              <div className="option-card">
                <div className="language-section">
                  <span className="language-label">Idioma</span>
                  <div className="language-buttons">
                    <button
                      type="button"
                      className={`language-btn ${formData.language === 'es' ? 'active' : ''}`}
                      onClick={() => setFormData(prev => ({ ...prev, language: 'es' }))}
                    >
                      🇪🇸 Español
                    </button>
                    <button
                      type="button"
                      className={`language-btn ${formData.language === 'en' ? 'active' : ''}`}
                      onClick={() => setFormData(prev => ({ ...prev, language: 'en' }))}
                    >
                      🇺🇸 English
                    </button>
                    <button
                      type="button"
                      className={`language-btn ${formData.language === 'fr' ? 'active' : ''}`}
                      onClick={() => setFormData(prev => ({ ...prev, language: 'fr' }))}
                    >
                      🇫🇷 Français
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Botón de envío */}
          <div className="submit-section">
            <button 
              type="submit" 
              className={`submit-button ${loading ? 'loading' : ''}`}
              disabled={loading || !formData.topic.trim()}
            >
              {loading ? (
                <>
                  <div className="loading-spinner"></div>
                  <span>Generando contenido científico...</span>
                </>
              ) : (                <>
                  <span>Generar Contenido PRO</span>
                </>
              )}
            </button>
          </div>
        </form>

        {/* Mostrar error */}
        {error && (
          <div className="error-card">
            <span className="error-text">{error}</span>
          </div>
        )}

        {/* Mostrar resultado */}
        {scientificData && (
          <div className="result-section">
            <div className="result-header">
              <h2 className="result-title">Contenido Científico Generado</h2>
              <div className="result-badge">PRO</div>
            </div>
            <div className="result-content">
              <h3>{scientificData.title}</h3>
              <p>{scientificData.content}</p>
              
              <div className="sources-section">
                <h4>Fuentes Científicas</h4>
                <ul className="sources-list">
                  {scientificData.sources.map((source, index) => (
                    <li key={index} className="source-item">{source}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MPPro;
