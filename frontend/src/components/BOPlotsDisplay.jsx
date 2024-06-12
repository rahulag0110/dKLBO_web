// src/components/BOPlotsDisplay.jsx
import React, { useState } from 'react';

const BOPlotsDisplay = ({ boPlots, onSatisfactionSubmit }) => {
  const validPlots = boPlots.filter((plot) => plot !== null).reverse();
  const [satisfaction, setSatisfaction] = useState(null);

  const handleSatisfactionChange = (event) => {
    setSatisfaction(event.target.value === 'yes');
  };

  const handleSubmit = () => {
    onSatisfactionSubmit(satisfaction);
  };

  return (
    <div>
      <h1>Bayesian Optimization Plots</h1>
      {validPlots.map((plot, index) => (
        <div key={index}>
          <img src={`data:image/png;base64,${plot}`} alt={`BO Plot ${index}`} style={{ width: '1000px' }} />
        </div>
      ))}
      <div>
        <h2>Are you Satisfied?</h2>
        <label>
          <input
            type="radio"
            name="satisfaction"
            value="yes"
            checked={satisfaction === true}
            onChange={handleSatisfactionChange}
          /> Yes
        </label>
        <label>
          <input
            type="radio"
            name="satisfaction"
            value="no"
            checked={satisfaction === false}
            onChange={handleSatisfactionChange}
          /> No
        </label>
        <button onClick={handleSubmit}>Submit</button>
      </div>
    </div>
  );
};

export default BOPlotsDisplay;
