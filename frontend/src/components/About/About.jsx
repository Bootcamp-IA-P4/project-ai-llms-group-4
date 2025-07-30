import React from 'react';
import './About.css';
import linkedinIcon from '../../assets/images/linkedin.svg';

const About = () => {  const teamMembers = [
    {
      name: "Stephany",
      role: "Frontend Developer",
      description: "Especialista en React y desarrollo de interfaces modernas",
      linkedinPhoto: "https://media.licdn.com/dms/image/v2/D4D03AQEuoD4ly_zB1Q/profile-displayphoto-shrink_800_800/B4DZUqi_4LHwAc-/0/1740175575379?e=1756339200&v=beta&t=-MhxxqQiQd74DKKynhUTeGjZkZybW0mE3D11QeaqMfY",
      linkedinUrl: "https://www.linkedin.com/in/stephyangeles"
    },
    {
      name: "Jose Luis", 
      role: "Backend Developer",
      description: "Experto en Python y desarrollo de APIs robustas",
      linkedinPhoto: "https://media.licdn.com/dms/image/v2/D4D03AQHPvoNKJfLVDA/profile-displayphoto-shrink_800_800/B4DZT.bi8UGkAc-/0/1739435422044?e=1756339200&v=beta&t=X9SSatlsx0gPGoHihQFevrS8hHl3Sb6-qDrCiyMOBTc",
      linkedinUrl: "https://www.linkedin.com/in/peperuiznieto/"
    },
    {
      name: "Cesar",
      role: "Database Developer",
      description: "Especialista en bases de datos y arquitectura de datos",
      linkedinPhoto: "https://media.licdn.com/dms/image/v2/D4D03AQFj6I5H2Fyp-w/profile-displayphoto-crop_800_800/B4DZe8x7vXH4AQ-/0/1751218896274?e=1756339200&v=beta&t=tSof5olv-CC_J5fbNvVDbQyvNndb5WmSFJR3sGviqqM",
      linkedinUrl: "https://www.linkedin.com/in/cesarmercadohernandez/"
    },
    {
      name: "Michael",
      role: "Scrum Master & IA Developer",
      description: "Gestión ágil de proyectos y desarrollo con inteligencia artificial",
      linkedinPhoto: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxaXRBuYybQO_PmPbnv-6uJSvMFDSj7NRAEw&s",
      linkedinUrl: "https://www.linkedin.com/in/michael-ejemplo"
    },
    {
      name: "Fernando",
      role: "IA Developer",
      description: "Especialista en modelos de lenguaje y generación de contenido",
      linkedinPhoto: "https://media.licdn.com/dms/image/v2/D4E35AQH2KOxPLjpY7A/profile-framedphoto-shrink_800_800/B4EZgYb8tIHIAs-/0/1752756636740?e=1753905600&v=beta&t=wCwXkF0aSxgPfVdyUT3EDevClV2w02b7us7JyhHwcwg",
      linkedinUrl: "https://www.linkedin.com/in/fernandogarciacatalan/"
    }
  ];

  return (
    <div className="about-container">
      <div className="about-content">
        <section className="about-intro">
          <h1 className="about-title">Acerca de MAGIC POST</h1>
          <p className="about-description">
            MAGIC POST es una aplicación revolucionaria que utiliza inteligencia artificial 
            para generar contenido creativo y atractivo para redes sociales. Nuestro objetivo 
            es democratizar la creación de contenido de calidad profesional, permitiendo a 
            usuarios de todos los niveles crear publicaciones impactantes con solo unos clics.
          </p>
          
          <div className="mission-section">
            <h2>Nuestra Misión</h2>
            <p>
              Queremos empoderar a creadores de contenido, emprendedores y empresas 
              proporcionándoles herramientas de IA que simplifiquen y mejoren su presencia 
              en redes sociales. Creemos que todos merecen tener acceso a contenido de 
              calidad profesional sin necesidad de conocimientos técnicos avanzados.
            </p>
          </div>

          <div className="features-section">
            <h2>¿Qué Hacemos?</h2>            <ul className="features-list">
              <li>Generación automática de contenido para múltiples plataformas</li>
              <li>Creación de imágenes personalizadas con IA</li>
              <li>Optimización específica para Instagram, LinkedIn y Twitter</li>
              <li>Interfaz intuitiva y fácil de usar</li>
              <li>Sugerencias creativas basadas en tendencias</li>
            </ul>
          </div>
        </section>

        <section className="team-section">
          <h2 className="team-title">Nuestro Equipo</h2>          <div className="team-grid">
            {teamMembers.map((member, index) => (
              <div key={index} className="team-member">
                <div className="member-content">
                  <div className="member-avatar">
                    <img 
                      src={member.linkedinPhoto} 
                      alt={`${member.name} - ${member.role}`}
                      className="member-photo"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                      }}
                    />
                    <div className="member-fallback" style={{display: 'none'}}>
                      <span className="member-initial">{member.name.charAt(0)}</span>
                    </div>
                  </div>
                  <h3 className="member-name">{member.name}</h3>
                  <p className="member-role">{member.role}</p>
                  <p className="member-description">{member.description}</p>
                </div>
                <a 
                  href={member.linkedinUrl} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="linkedin-link"
                  aria-label={`Ver perfil de LinkedIn de ${member.name}`}
                >
                  <img src={linkedinIcon} alt="LinkedIn" className="linkedin-icon" />
                  <span>Ver Perfil</span>
                </a>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default About;
