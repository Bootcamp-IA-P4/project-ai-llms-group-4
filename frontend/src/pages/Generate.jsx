import React, { useState } from 'react';
import ContentForm from '../components/Form/ContentForm';
import ContentResult from '../components/Form/ContentResult';
import { generateContent } from '../api';

const Generate = () => {
  const [contentResult, setContentResult] = useState(null);
  const [promptUsed, setPromptUsed] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    try {
      const data = await generateContent(formData);
      
      setContentResult(data.text);
      setImageUrl(data.image_url);
      setPromptUsed('Prompt generado por IA');
    } catch (error) {
      console.error('Error al generar contenido:', error);
      setError('Lo sentimos, ha ocurrido un error al generar el contenido. Por favor intente nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="content-wrapper">
        <header className="main-header">
          <h1 className="main-title" id="main-title" data-text="MAGIC POST GENERATOR">
            <span className="visually-hidden">MAGIC POST GENERATOR - Generador de Contenidos con IA</span>
            <span aria-hidden="true">MAGIC POST GENERATOR</span>
          </h1>
          <p className="main-description" id="main-description">
            Configura los parámetros para generar contenido optimizado para tu audiencia y plataforma
          </p>
        </header>
        
        <section className="form-section" aria-label="Formulario de generación de contenido">
          <ContentForm onSubmit={handleFormSubmit} loading={loading} />
        </section>
        
        {error && (
          <div className="error-message">
            <p>{error}</p>
            <button onClick={() => setError(null)}>Cerrar</button>
          </div>
        )}
        
        {contentResult && !error && (
          <section className="results-section">
            <ContentResult 
              content={contentResult}
              prompt={promptUsed}
              imageUrl={imageUrl}
            />
          </section>
        )}
      </div>
    </div>
  );
};

export default Generate;
