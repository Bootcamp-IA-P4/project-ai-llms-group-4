import React, { useState, useEffect, useRef } from 'react';
import './Header.css';

const Header = ({ currentView, onNavigate }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isFooterVisible, setIsFooterVisible] = useState(false);
  const headerRef = useRef(null);

  const handleNavClick = (e, view) => {
    e.preventDefault();
    if (onNavigate) {
      onNavigate(view);
    }
    setIsMenuOpen(false); // Close menu on navigation
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (headerRef.current && !headerRef.current.contains(event.target)) {
        setIsMenuOpen(false);
      }
    };

    if (isMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      // Prevent body scroll when menu is open
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.body.style.overflow = 'unset';
    };
  }, [isMenuOpen]);
  // Detect footer visibility for sticky header behavior
  useEffect(() => {
    const handleScroll = () => {
      const footer = document.querySelector('.app-footer');
      const header = headerRef.current;
      
      if (footer && header) {
        const footerRect = footer.getBoundingClientRect();
        const headerHeight = header.offsetHeight;
        const windowHeight = window.innerHeight;
        
        // Calculate if we should stop the sticky header at the footer
        const footerTopPosition = footerRect.top;
        const shouldStopAtFooter = footerTopPosition <= headerHeight;
        
        setIsFooterVisible(shouldStopAtFooter);
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    // Initial check
    handleScroll();
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);
  // Close menu on window resize
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768) {
        setIsMenuOpen(false);
      }
    };

    const handleKeyDown = (event) => {
      if (event.key === 'Escape' && isMenuOpen) {
        setIsMenuOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    document.addEventListener('keydown', handleKeyDown);
    
    return () => {
      window.removeEventListener('resize', handleResize);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isMenuOpen]);  return (
    <header 
      className={`app-header ${isMenuOpen ? 'menu-active' : ''} ${isFooterVisible ? 'footer-visible' : ''}`} 
      ref={headerRef}
    >
      <div className="container header-container">
        <div className="logo-container">
           <h1 className="magic-title" data-text="MAGIC POST">
            <span className="visually-hidden">MAGIC POST - Generador de Contenidos con IA</span>
            <span aria-hidden="true">MAGIC POST</span>
          </h1>
        </div>
        
        <button 
          className="menu-toggle"
          onClick={toggleMenu}
          aria-label="Toggle navigation menu"
          aria-expanded={isMenuOpen}
        >
          <span className={`hamburger ${isMenuOpen ? 'active' : ''}`}>
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>
          <nav className={`main-nav ${isMenuOpen ? 'active' : ''}`}>
          <div className="nav-header">
            <h3>Navegación</h3>
            <button 
              className="nav-close-btn"
              onClick={() => setIsMenuOpen(false)}
              aria-label="Cerrar menú"
            >
              ×
            </button>
          </div>
          <ul>
            <li>
              <a 
                href="/" 
                className={`nav-link ${currentView === 'home' ? 'active' : ''}`}
                onClick={(e) => handleNavClick(e, 'home')}
              >
                Inicio
              </a>
            </li>            <li>
              <a 
                href="/pro" 
                className={`nav-link ${currentView === 'mp-pro' ? 'active' : ''}`}
                onClick={(e) => handleNavClick(e, 'mp-pro')}
              >
                MP PRO
              </a>
            </li>
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
