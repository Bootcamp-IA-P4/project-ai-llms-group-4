import React from 'react';
import './Header.css';

const Header = ({ currentView, onNavigate }) => {
  const handleNavClick = (e, view) => {
    e.preventDefault();
    if (onNavigate) {
      onNavigate(view);
    }
  };

  return (
    <header className="app-header">
      <div className="container header-container">
        <div className="logo-container">
           <h1 className="magic-title" data-text="MAGIC POST">
            <span className="visually-hidden">MAGIC POST - Generador de Contenidos con IA</span>
            <span aria-hidden="true">MAGIC POST</span>
          </h1>
        </div>        
        <nav className="main-nav">
          <ul>
            <li>
              <a 
                href="/" 
                className={`nav-link ${currentView === 'home' ? 'active' : ''}`}
                onClick={(e) => handleNavClick(e, 'home')}
              >
                Inicio
              </a>
            </li>
            <li><a href="/docs" className="nav-link">Documentación</a></li>
            <li>
              <a 
                href="/about" 
                className={`nav-link ${currentView === 'about' ? 'active' : ''}`}
                onClick={(e) => handleNavClick(e, 'about')}
              >
                Acerca de
              </a>
            </li>
            <li><a href="/contact" className="nav-link contact-btn">Contacto</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
