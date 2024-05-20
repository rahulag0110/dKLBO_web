// src/components/PlotDisplay.jsx
import React from 'react';

const PlotDisplay = ({ plotData }) => {
  return (
    <div>
      <h2>Current Plot</h2>
      <img src={`data:image/png;base64,${plotData.plot}`} alt="Current Plot" style={{ width: '1000px' }} />
    </div>
  );
};

export default PlotDisplay;
