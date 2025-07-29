import React from 'react';
import './ModelSelector.css';

const ModelSelector = ({ selected, onChange }) => {
  const models = [
    { id: 'llama', name: 'LLaMA 3 (8B)', value: 'meta-llama/llama-3-8b-instruct' },
    { id: 'mistral', name: 'Mistral 7B', value: 'mistralai/mistral-7b-instruct' }
  ];

  const handleChange = (e) => {
    onChange({
      target: {
        name: 'model',
        value: e.target.value
      }
    });
  };

  return (
    <div className="model-selector">
      {models.map((model) => (
        <div className="model-option" key={model.id}>
          <input
            type="radio"
            id={`model-${model.id}`}
            name="model-selector"
            value={model.value}
            checked={selected === model.value}
            onChange={handleChange}
            className="model-radio"
          />
          <label htmlFor={`model-${model.id}`} className="model-label">
            <span className="model-name">{model.name}</span>
          </label>
        </div>
      ))}
    </div>
  );
};

export default ModelSelector;