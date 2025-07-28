import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const Home = () => {
  return (
    <div className="container">
      <div className="content-wrapper">
        <motion.header 
          className="main-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="main-title" id="main-title" data-text="MAGIC POST GENERATOR">
            <span className="visually-hidden">MAGIC POST GENERATOR - Generador de Contenidos con IA</span>
            <span aria-hidden="true">MAGIC POST GENERATOR</span>
          </h1>
          <p className="main-description" id="main-description">
            La herramienta de IA más avanzada para crear contenido optimizado para redes sociales y plataformas digitales
          </p>
        </motion.header>

        <motion.section 
          className="intro-section"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <div className="intro-content">
            <h2>¿Qué hace Magic Post Generator?</h2>
            <div className="features-grid">
              <div className="feature-card">
                <div className="feature-icon">🎯</div>
                <h3>Contenido Personalizado</h3>
                <p>Genera posts optimizados para diferentes plataformas como Instagram, Twitter, LinkedIn y blogs, adaptados a tu audiencia específica.</p>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">🤖</div>
                <h3>IA Avanzada</h3>
                <p>Utiliza modelos de lenguaje de última generación como Mistral, Llama y GPT para crear contenido de alta calidad y relevante.</p>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">📊</div>
                <h3>Noticias Financieras</h3>
                <p>Genera noticias financieras profesionales con datos actualizados del mercado para empresas específicas.</p>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">🔍</div>
                <h3>Búsqueda Semántica</h3>
                <p>Encuentra contenido similar y gestiona documentos para mejorar la precisión de las generaciones.</p>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">🎨</div>
                <h3>Múltiples Tonos</h3>
                <p>Desde profesional hasta humorístico, adapta el tono de tu contenido para conectar mejor con tu audiencia.</p>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">🌍</div>
                <h3>Multiidioma</h3>
                <p>Genera contenido en español, inglés, francés e italiano para alcanzar audiencias globales.</p>
              </div>
            </div>
          </div>
        </motion.section>

        <motion.section 
          className="cta-section"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <h2>Comienza a crear contenido increíble</h2>
          <div className="cta-buttons">
            <Link to="/generate" className="cta-button primary">
              MP GENERADOR
            </Link>
            <Link to="/finance" className="cta-button secondary">
              MP FINANZAS
            </Link>
            <Link to="/pro" className="cta-button tertiary">
              MP PRO⭐
            </Link>
          </div>
        </motion.section>
      </div>
    </div>
  );
};

export default Home;