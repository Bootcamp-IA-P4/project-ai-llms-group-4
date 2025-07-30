import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { generateFinancialNews, getFinancialNews } from '../api';
import './FinancePage.css';
import ButtonSelector from '../components/Form/ButtonSelector';

const FinancePage = () => {
  const [formData, setFormData] = useState({
    topic: '',
    company: '',
    language: ''
  });
  
  const [newsResult, setNewsResult] = useState(null);
  const [allNews, setAllNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingNews, setLoadingNews] = useState(false);
  const [error, setError] = useState(null);

  const languages = ['Español', 'Inglés', 'Francés', 'Italiano'];

  useEffect(() => {
    loadAllNews();
  }, []);

  const loadAllNews = async () => {
    setLoadingNews(true);
    try {
      const data = await getFinancialNews(10);
      setAllNews(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error cargando noticias:', error);
      setAllNews([]);
    } finally {
      setLoadingNews(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const data = await generateFinancialNews(formData.topic, formData.company, formData.language);
      setNewsResult(data);
      // Recargar todas las noticias después de generar una nueva
      loadAllNews();
    } catch (error) {
      console.error('Error al generar noticia financiera:', error);
      setError('Lo sentimos, ha ocurrido un error al generar la noticia financiera. Por favor intente nuevamente.');
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="container finance-page">
      <div className="content-wrapper">
        <motion.header 
          className="main-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="main-title" id="main-title" data-text="MAGIC POST GENERATOR">
            <span className="visually-hidden">MAGIC POST GENERATOR - MP Financiers</span>
            <span aria-hidden="true">MAGIC POST FINANCIERA</span>
          </h1>
          <p className="main-description" id="main-description">
            Genera noticias financieras profesionales con datos actualizados del mercado
          </p>
        </motion.header>

        <motion.section 
          className="form-section"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <div className="form-container">
            <form onSubmit={handleSubmit} className="content-form finance-form-compact">
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="topic" className="form-label">Tema financiero</label>
                  <input
                    type="text"
                    id="topic"
                    name="topic"
                    value={formData.topic}
                    onChange={handleChange}
                    className="form-input"
                    placeholder="Ej: acciones, criptomonedas, inflación, resultados trimestrales, fusiones, bonos verdes, mercados emergentes"
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="company" className="form-label">Empresa</label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    className="form-input"
                    placeholder="Ej: Nike, Apple, Tesla, Amazon, BBVA, Santander, Mercado Libre, Petrobras"
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="language" className="form-label">Idioma</label>
                  <ButtonSelector
                    options={languages}
                    selected={formData.language}
                    onChange={handleChange}
                    name="language"
                  />
                </div>
              </div>
              <button 
                type="submit" 
                className={`submit-button ${loading ? 'loading' : ''}`}
                disabled={loading}
              >
                {loading ? 'Generando...' : 'Generar Noticia Financiera'}
              </button>
            </form>
          </div>
        </motion.section>

        {error && (
          <motion.div 
            className="error-message"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <p>{error}</p>
            <button onClick={() => setError(null)} className="close-btn">Cerrar</button>
          </motion.div>
        )}

        {newsResult && !error && (
          <motion.section 
            className="results-section"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="result-container">
              <h3 className="result-title">Noticia Generada</h3>
              <div className="news-content">
                <div className="news-header">
                  <span className="news-symbol">{newsResult.symbol}</span>
                  <span className="news-timestamp">
                    {new Date(newsResult.timestamp).toLocaleString()}
                  </span>
                </div>
                {/* Mostrar imagen si existe */}
                {newsResult.image_url && (
                  <div className="news-image">
                    <img
                      src={`http://localhost:8000${newsResult.image_url}`}
                      alt="Imagen generada"
                      style={{ maxWidth: '100%', borderRadius: '12px', margin: '16px 0' }}
                    />
                  </div>
                )}
                <div className="news-body">
                  {newsResult.news_content?.split('\n').map((paragraph, index) => (
                    paragraph ? <p key={index}>{paragraph}</p> : <br key={index} />
                  ))}
                </div>
              </div>
            </div>
          </motion.section>
        )}

        <motion.section 
          className="all-news-section"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <div className="news-list-container">
            <div className="news-list-header">
              <h3>Noticias Financieras Recientes</h3>
              <button 
                onClick={loadAllNews} 
                className="refresh-btn"
                disabled={loadingNews}
              >
                {loadingNews ? '🔄' : '🔃'} Actualizar
              </button>
            </div>
            {loadingNews ? (
              <div className="loading-news">Cargando noticias...</div>
            ) : allNews.length > 0 ? (
              <div className="news-table-wrapper">
                <table className="news-table">
                  <thead>
                    <tr className="news-table-header-row">
                      <th className="news-th-topic">Tema</th>
                      <th className="news-th-company">Empresa</th>
                      <th className="news-th-language">Idioma</th>
                      <th className="news-th-actions">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {allNews.map((news, index) => (
                      <tr key={index}>
                        <td>{news.topic || '-'}</td>
                        <td>{news.symbol || '-'}</td>
                        <td>{news.language || '-'}</td>
                        <td>
                          <button className="table-btn view-btn" title="Ver detalle" onClick={() => setNewsResult(news)}>👁️</button>
                          <button className="table-btn copy-btn" title="Copiar" onClick={() => navigator.clipboard.writeText(news.news_content || '')}>📋</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="no-news">No hay noticias disponibles</div>
            )}
          </div>
        </motion.section>
      </div>
    </div>
  );
};

export default FinancePage;
