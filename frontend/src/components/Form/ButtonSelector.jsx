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
      {options.map((option) => (
        <button
          key={option}
          type="button"
          className={`selector-button ${selected === option ? 'active' : ''}`}
          onClick={() => handleClick(option)}
        >
          <span>{option}</span>
        </button>
      ))}
    </div>
  );
};

export default ButtonSelector;