// src/components/BOPlotsDisplay.jsx
import React, { useState } from 'react';
import '../styles/BOPlotsDisplay.css';

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
    <div className="bo-plots-container">
      <p className="description">BO currently with human in the loop</p>
      <h2>Estimation after initial evaluation</h2>
      {validPlots.map((plot, index) => (
        <div key={index}>
          <img src={`data:image/png;base64,${plot}`} alt={`BO Plot ${index}`} style={{ width: '1000px' }} />
        </div>
      ))}
      <div className="satisfaction-container">
        <h2>Are you satisfied?</h2>
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
