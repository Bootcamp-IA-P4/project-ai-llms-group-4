import React from 'react';
import './ContactPage.css';

const ContactPage = () => {
  return (
    <div className="contact-page">
      <div className="container">
        <div className="contact-content">
          <header className="contact-header">
            <h1>Contacto</h1>
            <p>¿Tienes alguna pregunta o necesitas ayuda? Estamos aquí para ayudarte.</p>
          </header>
          
          <div className="contact-grid">
            <div className="contact-info">
              <h2>Información de Contacto</h2>
              <div className="contact-item">
                <h3>📧 Email</h3>
                <p>contacto@magicpost.com</p>
              </div>
              <div className="contact-item">
                <h3>🎓 Soporte Académico</h3>
                <p>Este proyecto es parte del IA Bootcamp</p>
              </div>
              <div className="contact-item">
                <h3>💬 Feedback</h3>
                <p>Valoramos tus comentarios para mejorar</p>
              </div>
            </div>
            
            <div className="contact-form-container">
              <h2>Envíanos un mensaje</h2>
              <form className="contact-form">
                <div className="form-group">
                  <label htmlFor="name">Nombre</label>
                  <input type="text" id="name" name="name" required />
                </div>
                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input type="email" id="email" name="email" required />
                </div>
                <div className="form-group">
                  <label htmlFor="subject">Asunto</label>
                  <input type="text" id="subject" name="subject" required />
                </div>
                <div className="form-group">
                  <label htmlFor="message">Mensaje</label>
                  <textarea id="message" name="message" rows="5" required></textarea>
                </div>
                <button type="submit" className="submit-btn">Enviar Mensaje</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;