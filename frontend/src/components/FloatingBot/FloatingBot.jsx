import React, { useState, useEffect } from 'react';
import './FloatingBot.css';
import BOT from '../../assets/images/BOT.png';

const FloatingBot = ({ onClose }) => {
  const [isVisible, setIsVisible] = useState(() => {
    const saved = localStorage.getItem('magicpost-bot-visible');
    return saved !== null ? JSON.parse(saved) : true;
  });
  const [position, setPosition] = useState(() => {
    const saved = localStorage.getItem('magicpost-bot-position');
    return saved ? JSON.parse(saved) : { x: 50, y: 50 };
  });const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });  const [showMessage, setShowMessage] = useState(false);
  const [newMessage, setNewMessage] = useState(false);
  const [clickStartTime, setClickStartTime] = useState(0);
  // Mensajes aleatorios que puede mostrar el bot
  const messages = [
    "¡Hola! 🤖",
    "¿Necesitas ayuda? 💡",
    "¡Crea posts increíbles! ✨",
    "¿Listo para crear? 🚀",
    "Estoy aquí 😊"
  ];

  const [currentMessage, setCurrentMessage] = useState(messages[0]);
  // Manejar el scroll para que el bot se mueva suavemente
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

  const handleMouseMove = (e) => {
    if (isDragging) {
      setPosition({
        x: Math.max(0, Math.min(window.innerWidth - 100, e.clientX - dragStart.x)),
        y: Math.max(0, Math.min(window.innerHeight - 100, e.clientY - dragStart.y))
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

  useEffect(() => {
    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
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