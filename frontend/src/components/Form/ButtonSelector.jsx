import React from 'react';
import './ButtonSelector.css';

const ButtonSelector = ({ options, selected, onChange, name }) => {
  const handleClick = (value) => {
    onChange({
      target: {
        name: name,
        value: value
      }
    });
  };
  return (
    <div className="button-selector">
      {options.map((option) => {
        // Si option es un objeto con icon y name, renderizar con icono
        if (typeof option === 'object' && option.icon && option.name) {
          return (
            <button
              key={option.name}
              type="button"
              className={`selector-button has-icon ${selected === option.name ? 'active' : ''}`}
              onClick={() => handleClick(option.name)}
            >
              <img src={option.icon} alt={`${option.name} icon`} className="selector-icon" />
              <span>{option.name}</span>
            </button>
          );
        }
        // Si option es un string simple, renderizar sin icono
        return (
          <button
            key={option}
            type="button"
            className={`selector-button ${selected === option ? 'active' : ''}`}
            onClick={() => handleClick(option)}
          >
            <span>{option}</span>
          </button>
        );
      })}
    </div>
  );
};

export default ButtonSelector;