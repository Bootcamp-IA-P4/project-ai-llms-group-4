import React, { useState } from 'react';
import { Tooltip } from 'react-tooltip';
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import ContentForm from './components/Form/ContentForm';
import ContentResult from './components/Form/ContentResult';
import FloatingBot from './components/FloatingBot/FloatingBot';
import About from './components/About/About';
import { generateContent } from './api';
import './styles/App.css';

function App() {
  const [contentResult, setContentResult] = useState(null);
  const [promptUsed, setPromptUsed] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentView, setCurrentView] = useState('home'); // 'home' or 'about'
  const [showBot, setShowBot] = useState(() => {
    const saved = localStorage.getItem('magicpost-bot-visible');
    return saved !== null ? JSON.parse(saved) : true;
  });

  const mainContentRef = React.useRef(null);
    const scrollToContent = () => {
    mainContentRef.current?.focus();
  };
  const handleRestoreBot = () => {
    setShowBot(true);
  };

  const handleNavigation = (view) => {
    setCurrentView(view);
    // Reset form state when navigating
    if (view === 'home') {
      setContentResult(null);
      setError(null);
    }
  };
  
  // Add skip link for accessibility

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    try {
      const data = await generateContent(formData);
      setContentResult(data.result);
      setPromptUsed(data.prompt);
      setImageUrl(data.imageUrl);
    } catch (error) {
      console.error('Error al generar contenido:', error);
      setError('Lo sentimos, ha ocurrido un error al generar el contenido. Por favor intente nuevamente.');
    } finally {
      setLoading(false);
    }
  };  return (
    <div className="app-container">
      <a href="#main-content" className="skip-to-content" onClick={scrollToContent}>
        Saltar al contenido principal
      </a>
      <Header currentView={currentView} onNavigate={handleNavigation} />
      
      <main className="main-content" id="main-content" ref={mainContentRef} tabIndex="-1">
        {currentView === 'home' ? (
          <div className="container">
            <div className="content-wrapper">
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
        ) : currentView === 'about' ? (
          <About />
        ) : null}
      </main>      
      <Tooltip id="tooltip-component" />
      <Footer onRestoreBot={handleRestoreBot} />
      {showBot && <FloatingBot onClose={() => setShowBot(false)} />}
    </div>
  );
}

export default App;
