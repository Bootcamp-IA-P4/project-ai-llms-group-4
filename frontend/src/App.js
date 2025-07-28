import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Tooltip } from 'react-tooltip';
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import FloatingBot from './components/FloatingBot/FloatingBot';
import Home from './pages/Home';
import Generate from './pages/Generate';
import AboutPage from './pages/AboutPage';
import MPProPage from './pages/MPProPage';
import ContactPage from './pages/ContactPage';
import FinancePage from './pages/FinancePage';
import './styles/App.css';

function App() {
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

  return (
    <Router>
      <div className="app-container">
        <a href="#main-content" className="skip-to-content" onClick={scrollToContent}>
          Saltar al contenido principal
        </a>
        <Header />
          <main className="main-content" id="main-content" ref={mainContentRef} tabIndex="-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/generate" element={<Generate />} />
            <Route path="/finance" element={<FinancePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/pro" element={<MPProPage />} />
            <Route path="/contact" element={<ContactPage />} />
          </Routes>
        </main>
        
        <Tooltip id="tooltip-component" />
        <Footer onRestoreBot={handleRestoreBot} />
        {showBot && <FloatingBot onClose={() => setShowBot(false)} />}
      </div>
    </Router>
  );
}

export default App;
