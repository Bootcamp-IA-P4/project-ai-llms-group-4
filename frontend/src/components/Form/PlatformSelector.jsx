import React from 'react';
import './PlatformSelector.css';

// Importar iconos
import twitterIcon from '../../assets/images/twitter.svg';
import linkedinIcon from '../../assets/images/linkedin.svg';
import instagramIcon from '../../assets/images/instagram.svg';
import blogIcon from '../../assets/images/blog.svg';

const PlatformSelector = ({ selected, onChange }) => {
  const platforms = [
    { id: 'twitter', name: 'Twitter', icon: twitterIcon },
    { id: 'linkedin', name: 'LinkedIn', icon: linkedinIcon },
    { id: 'instagram', name: 'Instagram', icon: instagramIcon },
    { id: 'blog', name: 'Blog', icon: blogIcon }
  ];

  const handleChange = (e) => {
    onChange({
      target: {
        name: 'platform',
        value: e.target.value
      }
    });
  };

  return (
    <div className="platform-selector">
      {platforms.map((platform) => (
        <div className="platform-option" key={platform.id}>
          <input
            type="radio"
            id={`platform-${platform.id}`}
            name="platform"
            value={platform.name}
            className="platform-radio"
            checked={selected === platform.name}
            onChange={handleChange}
          />
          <label htmlFor={`platform-${platform.id}`} className="platform-label">
            <img
              src={platform.icon}
              alt={`${platform.name} icon`}
              className="platform-icon"
            />
            <span className="platform-name">{platform.name}</span>
          </label>
        </div>
      ))}
    </div>
  );
};

export default PlatformSelector;
