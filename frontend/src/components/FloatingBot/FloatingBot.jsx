import React, { useState, useEffect } from 'react';
import './FloatingBot.css';
import BOT from '../../assets/images/BOT.png';

const FloatingBot = ({ onClose }) => {
  const [isVisible, setIsVisible] = useState(() => {
    const saved = localStorage.getItem('magicpost-bot-visible');
    return saved !== null ? JSON.parse(saved) : true;
  });  const [position, setPosition] = useState(() => {
    const saved = localStorage.getItem('magicpost-bot-position');
    if (saved) {
      return JSON.parse(saved);
    }
    // Posición por defecto optimizada para móvil
    const isMobile = window.innerWidth <= 768;
    if (isMobile) {
      return { 
        x: window.innerWidth - 110, // 110px desde el borde derecho (espacio para el bot de 90px + margen)
        y: window.innerHeight - 180 // 180px desde abajo para evitar interfaz
      };
    }
    return { x: 50, y: 50 };
  });const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });  const [showMessage, setShowMessage] = useState(false);
  const [newMessage, setNewMessage] = useState(false);
  const [clickStartTime, setClickStartTime] = useState(0);
  // Mensajes aleatorios que puede mostrar el bot
  const messages = [
    "¡Hola! 🤖",
    "¿Necesitas ayuda? 💡",
    "¡Crea posts increíbles!",
    "¿Listo para crear? 🚀",
    "Estoy aquí 😊"
  ];

  const [currentMessage, setCurrentMessage] = useState(messages[0]);  // Manejar el scroll para que el bot se mueva suavemente
  useEffect(() => {
    const handleScroll = () => {
      if (!isDragging) {
        const scrollY = window.scrollY;
        setPosition(prev => ({
          ...prev,
          y: Math.max(50, Math.min(window.innerHeight - 120, 50 + scrollY * 0.1))
        }));
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [isDragging]);

  // Manejar cambios de tamaño de ventana para mantener el bot visible
  useEffect(() => {
    const handleResize = () => {
      const botSize = window.innerWidth <= 480 ? 90 : (window.innerWidth <= 768 ? 100 : 120);
      setPosition(prev => ({
        x: Math.max(0, Math.min(window.innerWidth - botSize, prev.x)),
        y: Math.max(0, Math.min(window.innerHeight - botSize, prev.y))
      }));
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
 
  useEffect(() => {
    const interval = setInterval(() => {
      const randomIndex = Math.floor(Math.random() * messages.length);
      setCurrentMessage(messages[randomIndex]);
      setNewMessage(true);
      setTimeout(() => setNewMessage(false), 2000);
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  // Mostrar mensaje al hacer hover
  const handleMouseEnter = () => {
    setShowMessage(true);
  };

  const handleMouseLeave = () => {
    setTimeout(() => setShowMessage(false), 1000);
  };
  // Funciones para arrastrar el bot
  const handleMouseDown = (e) => {
    setClickStartTime(Date.now());
    setIsDragging(true);
    setDragStart({
      x: e.clientX - position.x,
      y: e.clientY - position.y
    });
  };

  // Soporte para touch en móviles
  const handleTouchStart = (e) => {
    e.preventDefault();
    setClickStartTime(Date.now());
    setIsDragging(true);
    const touch = e.touches[0];
    setDragStart({
      x: touch.clientX - position.x,
      y: touch.clientY - position.y
    });
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      const botSize = window.innerWidth <= 480 ? 90 : (window.innerWidth <= 768 ? 100 : 120);
      setPosition({
        x: Math.max(0, Math.min(window.innerWidth - botSize, e.clientX - dragStart.x)),
        y: Math.max(0, Math.min(window.innerHeight - botSize, e.clientY - dragStart.y))
      });
    }
  };

  const handleTouchMove = (e) => {
    if (isDragging) {
      e.preventDefault();
      const touch = e.touches[0];
      const botSize = window.innerWidth <= 480 ? 90 : (window.innerWidth <= 768 ? 100 : 120);
      setPosition({
        x: Math.max(0, Math.min(window.innerWidth - botSize, touch.clientX - dragStart.x)),
        y: Math.max(0, Math.min(window.innerHeight - botSize, touch.clientY - dragStart.y))
      });
    }
  };

  const handleMouseUp = () => {
    const clickDuration = Date.now() - clickStartTime;
      // Si fue un clic rápido (menos de 200ms) y no se movió mucho, mostrar mensaje especial
    if (clickDuration < 200 && !isDragging) {
      const helpMessages = [
        "💡 Tip: Múltiples redes sociales",
        "🎨 Consejo: Activa imágenes",
        "🌍 Recuerda: Cambia idioma",
        "🚀 Truco: Varía el tono"
      ];
      const randomTip = helpMessages[Math.floor(Math.random() * helpMessages.length)];
      setCurrentMessage(randomTip);
      setShowMessage(true);
      setTimeout(() => setShowMessage(false), 5000);
    }
    
    setIsDragging(false);
  };

  const handleTouchEnd = () => {
    const clickDuration = Date.now() - clickStartTime;
    // Si fue un toque rápido (menos de 200ms) y no se movió mucho, mostrar mensaje especial
    if (clickDuration < 200 && !isDragging) {
      const helpMessages = [
        "💡 Tip: Múltiples redes sociales",
        "🎨 Consejo: Activa imágenes",
        "🌍 Recuerda: Cambia idioma",
        "🚀 Truco: Varía el tono"
      ];
      const randomTip = helpMessages[Math.floor(Math.random() * helpMessages.length)];
      setCurrentMessage(randomTip);
      setShowMessage(true);
      setTimeout(() => setShowMessage(false), 5000);
    }
    
    setIsDragging(false);
  };

  useEffect(() => {
    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
      window.addEventListener('touchmove', handleTouchMove, { passive: false });
      window.addEventListener('touchend', handleTouchEnd);
    }

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
      window.removeEventListener('touchmove', handleTouchMove);
      window.removeEventListener('touchend', handleTouchEnd);
    };
  }, [isDragging, dragStart]);  const closeBotHandler = () => {
    setIsVisible(false);
    localStorage.setItem('magicpost-bot-visible', 'false');
    if (onClose) {
      onClose();
    }
  };

  // Guardar posición cuando se mueva
  useEffect(() => {
    localStorage.setItem('magicpost-bot-position', JSON.stringify(position));
  }, [position]);

  if (!isVisible) return null;  return (
    <div 
      className={`floating-bot ${isDragging ? 'dragging' : ''} ${newMessage ? 'new-message' : ''}`}
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`
      }}
      onMouseDown={handleMouseDown}
      onTouchStart={handleTouchStart}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <button 
        className="close-btn" 
        onClick={closeBotHandler}
        onMouseDown={(e) => e.stopPropagation()}
        title="Cerrar bot"
      >
        ×
      </button>
      <img 
        src={BOT} 
        alt="MAGIC POST Bot" 
        className="bot-image"
        draggable={false}
      />
      <div className={`bot-tooltip ${showMessage ? 'show' : ''}`}>
        {currentMessage}
      </div>
    </div>
  );
};

export default FloatingBot;