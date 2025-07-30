import React, { useState } from 'react';
import { ingestArxivPapers, queryArxivContent } from '../api';
import '../components/MPPro/MPPro.css';

const MPPro = () => {
  const [loading, setLoading] = useState(false);
  const [scientificData, setScientificData] = useState(null);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState('');
  const [formData, setFormData] = useState({
    topic: '',
    max_papers: 3,
    question: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setCurrentStep('');
    
    try {
      // Paso 1: Ingestar papers científicos
      setCurrentStep(`Buscando papers sobre "${formData.topic}"...`);
      console.log('Ingesting papers for topic:', formData.topic);
      
      const ingestResult = await ingestArxivPapers(formData.topic, parseInt(formData.max_papers));
      console.log('Ingest result:', ingestResult);
      
      if (!ingestResult.message || ingestResult.message.includes('No se encontraron papers')) {
        throw new Error('No se encontraron papers científicos para este tema. Intenta con términos más específicos o en inglés.');
      }

      // Paso 2: Consultar contenido basado en los papers
      setCurrentStep('Analizando papers científicos...');
      console.log('Querying with question:', formData.question);
      
      const queryResult = await queryArxivContent(formData.question);
      console.log('Query result:', queryResult);

      if (!queryResult.answer) {
        throw new Error('No se pudo generar contenido basado en los papers.');
      }

      // Procesar resultados
      setCurrentStep('Contenido científico generado');
      const papersCount = ingestResult.message.match(/(\d+)/)?.[0] || formData.max_papers;
      
      setScientificData({
        title: `Análisis Científico: ${formData.topic}`,
        content: queryResult.answer,
        question: formData.question,
        sources: [
          `${papersCount} papers científicos de ArXiv analizados`,
          `Investigación sobre ${formData.topic}`,
          `Base de datos científica - ArXiv.org`
        ],
        papersAnalyzed: papersCount
      });

    } catch (err) {
      console.error('Error en proceso científico:', err);
      setError(err.message || 'Error al generar contenido científico.');
      setCurrentStep('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mp-pro-container">
      <div className="mp-pro-content">
        <header className="mp-pro-header">
          <h1 className="mp-pro-title">
            <span className="visually-hidden">MAGIC POST PRO - Generador de Contenidos Científicos</span>
            <span aria-hidden="true">MAGIC POST PRO</span>
          </h1>
          <p className="mp-pro-subtitle">
            Análisis científico basado en papers reales de ArXiv
          </p>
        </header>

        <form onSubmit={handleSubmit} className="mp-pro-form">
          <div className="form-section">
            <label className="form-label">
              <span className="label-text">Tema de Investigación</span>
            </label>
            <input
              type="text"
              name="topic"
              value={formData.topic}
              onChange={handleInputChange}
              placeholder="machine learning, quantum computing, neural networks..."
              className="form-input"
              required
            />
            <small className="form-help">
              Usa términos en inglés para mejores resultados
            </small>
          </div>

          <div className="form-section">
            <label className="form-label">
              <span className="label-text">Número de Papers a Analizar</span>
            </label>
            <select
              name="max_papers"
              value={formData.max_papers}
              onChange={handleInputChange}
              className="form-select"
            >
              <option value={1}>1 paper</option>
              <option value={3}>3 papers</option>
              <option value={5}>5 papers</option>
            </select>
          </div>

          <div className="form-section">
            <label className="form-label">
              <span className="label-text">Pregunta Científica</span>
            </label>
            <textarea
              name="question"
              value={formData.question}
              onChange={handleInputChange}
              placeholder="¿Qué aspectos específicos quieres analizar sobre este tema? Ej: Explica las últimas aplicaciones en medicina, analiza el estado actual de la investigación..."
              className="form-textarea"
              rows={4}
              required
            />
            <small className="form-help">
              Formula una pregunta específica sobre el tema para obtener un análisis más preciso
            </small>
          </div>

          <div className="submit-section">
            <button 
              type="submit" 
              className={`submit-button ${loading ? 'loading' : ''}`}
              disabled={loading || !formData.topic.trim() || !formData.question.trim()}
            >
              {loading ? (
                <>
                  <div className="loading-spinner"></div>
                  <span>Procesando papers científicos...</span>
                </>
              ) : (
                <span>Generar Análisis Científico</span>
              )}
            </button>
            
            {currentStep && (
              <div className="progress-message">
                {currentStep}
              </div>
            )}
          </div>
        </form>

        {error && (
          <div className="error-card">
            <span className="error-text">{error}</span>
            <button 
              onClick={() => setError(null)} 
              className="error-close-btn"
            >
              Cerrar
            </button>
          </div>
        )}

        {scientificData && (
          <div className="result-section">
            <div className="result-header">
              <h2 className="result-title">Análisis Científico</h2>
              <div className="result-badge">PRO</div>
            </div>
            
            <div className="result-content">
              <h3>{scientificData.title}</h3>
              
              <div className="analysis-metadata">
                <div className="metadata-item">
                  <strong>Papers analizados:</strong> {scientificData.papersAnalyzed}
                </div>
                <div className="metadata-item">
                  <strong>Pregunta:</strong> {scientificData.question}
                </div>
              </div>
              
              <div className="scientific-content">
                {scientificData.content.split('\n').map((paragraph, index) => (
                  paragraph.trim() ? <p key={index}>{paragraph}</p> : <br key={index} />
                ))}
              </div>
              
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