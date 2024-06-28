// src/components/PlotDisplay.jsx
import React from 'react';
import '../styles/InitialEvalVoting.css'; // Ensure the path matches your structure

const PlotDisplay = ({ plotData }) => {
  return (
    <div className="evaluation-section">
      <h2>Current Plot</h2>
      <img src={`data:image/png;base64,${plotData.plot}`} alt="Current Plot" />
    </div>
  );
};

export default PlotDisplay;
