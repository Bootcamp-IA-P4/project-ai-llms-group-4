import React from 'react';
import './Footer.css';

const Footer = ({ onRestoreBot }) => {
  const currentYear = new Date().getFullYear();
  
  const handleRestoreBot = () => {
    if (onRestoreBot) {
      onRestoreBot();
      localStorage.setItem('magicpost-bot-visible', 'true');
    }
  };

  return (
    <footer className="app-footer">
      <div className="container footer-container">
        <div className="footer-grid">
          <div className="footer-section">
            <h4>Generador de Contenido IA</h4>
            <p>
              Tecnología de vanguardia para la creación de contenido optimizado
              para diferentes plataformas sociales y audiencias.
            </p>
          </div>
          
          <div className="footer-section">
            <h4>Enlaces rápidos</h4>
            <ul className="footer-links">
              <li><a href="#">Inicio</a></li>
              <li><a href="#">Características</a></li>
              <li><a href="#">Modelos IA</a></li>
              <li><a href="#">Precios</a></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4>Recursos</h4>
            <ul className="footer-links">
              <li><a href="#">Documentación</a></li>
              <li><a href="#">API</a></li>
              <li><a href="#">Tutoriales</a></li>
              <li><a href="#">Blog</a></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4>Contacto</h4>
            <ul className="footer-links">
              <li><a href="#">Soporte</a></li>
              <li><a href="#">Ventas</a></li>
              <li><a href="#">Reportar problema</a></li>
              <li><a href="#">Feedback</a></li>
            </ul>
          </div>
        </div>
          <div className="footer-bottom">
          <p>© {currentYear} Generador de Contenido IA. Todos los derechos reservados.</p>
          {localStorage.getItem('magicpost-bot-visible') === 'false' && (
            <button className="restore-bot-btn" onClick={handleRestoreBot} title="Restaurar asistente bot">
              🤖 Restaurar Bot
            </button>
          )}
        </div>
      </div>
    </footer>
  );
};

export default Footer;
