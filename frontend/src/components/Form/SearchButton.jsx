import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { searchContent, getRecentPosts } from '../../api';
import './SearchButton.css';
import RainbowSearchIcon from '../../assets/images/blog.svg';

const SearchButton = ({ onContentSelect }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [previousPosts, setPreviousPosts] = useState([]);
  const [loadingPrevious, setLoadingPrevious] = useState(false);
  
  // Estados para feedback visual
  const [selectedPosts, setSelectedPosts] = useState([]);
  const [feedbackMessage, setFeedbackMessage] = useState('');

  // Función para obtener publicaciones anteriores
  const fetchPreviousPosts = async () => {
    setLoadingPrevious(true);
    try {
      const results = await getRecentPosts(10);
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

  // Función sin preventDefault (ya no es un form)
  const handleSearch = async () => {
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

  // Manejar Enter en el input
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSearch();
    }
  };

  // Función con feedback visual
  const handleSelectContent = (content) => {
    const contentText = content.content || content.text || content;
    
    if (onContentSelect) {
      onContentSelect(contentText);
    }
    
    // Agregar a la lista de seleccionados
    const truncatedText = contentText.length > 50 
      ? contentText.substring(0, 50) + '...' 
      : contentText;
    
    setSelectedPosts(prev => [...prev, truncatedText]);
    setFeedbackMessage('✅ Contenido cargado como inspiración');
    
    // Auto-limpiar mensaje después de 3 segundos
    setTimeout(() => {
      setFeedbackMessage('');
    }, 3000);
  };

  const clearSearch = () => {
    setSearchQuery('');
    setSearchResults([]);
  };

  // Función para cerrar y limpiar todo
  const handleClose = () => {
    setIsExpanded(false);
    setFeedbackMessage('');
  };

  return (
    <div className="search-button-container">
      {/* Overlay modal para el panel de búsqueda */}
      {isExpanded && <div className="search-modal-overlay" onClick={handleClose} />}
      
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

      {/* Lista de posts seleccionados */}
      {selectedPosts.length > 0 && (
        <div className="selected-posts-list">
          <h5>Posts usados como inspiración:</h5>
          {selectedPosts.map((postText, index) => (
            <div key={index} className="selected-post-item">
              📄 {postText}
            </div>
          ))}
        </div>
      )}

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
                onClick={handleClose}
                aria-label="Cerrar"
              >
                ×
              </button>
            </div>
            
            {/* ✅ CAMBIO: div en lugar de form */}
            <div className="search-form">
              <div className="search-input-group">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={handleKeyPress} 
                  placeholder="Buscar por tema, palabras clave..."
                  className="search-input"
                  disabled={searchLoading}
                />
                <div className="search-buttons">
                  <button 
                    type="button" 
                    className="search-btn rainbow-btn"
                    onClick={handleSearch} 
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
            </div>

            {/* Mensaje de feedback */}
            {feedbackMessage && (
              <div className="feedback-message success">
                {feedbackMessage}
              </div>
            )}

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

            {/* Botón para cerrar con confirmación */}
            <div className="search-actions">
              <button 
                type="button" 
                className="close-search-btn rainbow-btn"
                onClick={handleClose}
              >
                {selectedPosts.length > 0 ? `Usar ${selectedPosts.length} post(s) como inspiración` : '🚪 Cerrar'}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default SearchButton;