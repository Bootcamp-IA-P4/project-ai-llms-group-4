import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { searchContent } from '../../api';
import './SearchButton.css';
import RainbowSearchIcon from '../../assets/images/blog.svg'; // Usa un SVG bonito si tienes, si no, reemplaza por un emoji o icono

const SearchButton = ({ onContentSelect }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [previousPosts, setPreviousPosts] = useState([]);
  const [loadingPrevious, setLoadingPrevious] = useState(false);

  // Función para obtener publicaciones anteriores
  const fetchPreviousPosts = async () => {
    setLoadingPrevious(true);
    try {
      // Buscar contenido general para obtener publicaciones anteriores
      const results = await searchContent('', 10); // Buscar las últimas 10 publicaciones
      setPreviousPosts(results);
    } catch (error) {
      console.error('Error obteniendo publicaciones anteriores:', error);
      setPreviousPosts([]);
    } finally {
      setLoadingPrevious(false);
    }
  };

  // Cargar publicaciones anteriores cuando se expande
  useEffect(() => {
    if (isExpanded && previousPosts.length === 0) {
      fetchPreviousPosts();
    }
  }, [isExpanded]);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setSearchLoading(true);
    try {
      const results = await searchContent(searchQuery, 5);
      setSearchResults(results);
    } catch (error) {
      console.error('Error en búsqueda:', error);
      setSearchResults([]);
    } finally {
      setSearchLoading(false);
    }
  };

  const handleSelectContent = (content) => {
    if (onContentSelect) {
      onContentSelect(content.content || content.text || content);
    }
    setIsExpanded(false);
  };

  const clearSearch = () => {
    setSearchQuery('');
    setSearchResults([]);
  };

  return (
    <div className="search-button-container">
      {/* Overlay modal para el panel de búsqueda */}
      {isExpanded && <div className="search-modal-overlay" onClick={() => setIsExpanded(false)} />}
      <button
        type="button"
        className={`search-toggle-btn rainbow-btn ${isExpanded ? 'active' : ''}`}
        onClick={() => setIsExpanded(!isExpanded)}
        disabled={searchLoading}
      >
        <img src={RainbowSearchIcon} alt="Buscar" className="search-icon-svg" />
        <span className="search-text">Buscar Posts</span>
        {searchLoading && <span className="loading-spinner">⏳</span>}
      </button>

      {isExpanded && (
        <div className="search-modal-centered">
          <motion.div 
            className="search-panel-modal"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            <div className="search-header">
              <h4>🔍 Buscar Publicaciones</h4>
              <button 
                className="close-search"
                onClick={() => setIsExpanded(false)}
                aria-label="Cerrar"
              >
                ×
              </button>
            </div>
            <form onSubmit={handleSearch} className="search-form">
              <div className="search-input-group">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Buscar por tema, palabras clave..."
                  className="search-input"
                  disabled={searchLoading}
                />
                <div className="search-buttons">
                  <button 
                    type="submit" 
                    className="search-btn rainbow-btn"
                    disabled={searchLoading || !searchQuery.trim()}
                  >
                    <img src={RainbowSearchIcon} alt="Buscar" className="search-icon-svg" />
                  </button>
                  {searchQuery && (
                    <button 
                      type="button" 
                      className="clear-btn"
                      onClick={clearSearch}
                    >
                      ✕
                    </button>
                  )}
                </div>
              </div>
            </form>
            {/* Resultados de búsqueda */}
            <div className="search-results-scroll">
              {searchResults.length > 0 && (
                <div className="search-results">
                  <h5>📋 Resultados de Búsqueda ({searchResults.length})</h5>
                  <div className="results-list">
                    {searchResults.map((result, index) => (
                      <div 
                        key={index} 
                        className="search-result-item"
                        onClick={() => handleSelectContent(result)}
                      >
                        {result.content || result.text || 'Sin contenido'}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {/* Publicaciones anteriores */}
              {previousPosts.length > 0 && !searchQuery && (
                <div className="previous-posts">
                  <h5>🕑 Publicaciones Recientes</h5>
                  <div className="results-list">
                    {previousPosts.map((post, index) => (
                      <div 
                        key={index} 
                        className="search-result-item"
                        onClick={() => handleSelectContent(post)}
                      >
                        {post.content || post.text || 'Sin contenido'}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {loadingPrevious && <div className="loading-news">Cargando publicaciones...</div>}
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default SearchButton;
