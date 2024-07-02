import React from 'react';
import '../styles/BOResults.css';

const BOResults = ({ optimResults, GPFigures, locationPlots, onReset }) => {
  const validGPFigures = GPFigures.filter((figure) => figure !== null);
  const validLocationPlots = locationPlots.filter((plot) => plot !== null);

  return (
    <div className="results-section">
      <h2>Exploration completed. See final results below</h2>
      <h2>GP figures</h2>
      <div className="gp-plot-grid">
        {validGPFigures.map((figure, index) => (
          <div key={index} className="plot-container">
            <h3>Estimation after iteration {index * 10}</h3>
            <img src={`data:image/png;base64,${figure}`} alt={`GP Figure ${index}`} />
          </div>
        ))}
      </div>
      <h2>Explored data autonomously</h2>
      <div className="location-plot-grid">
        {validLocationPlots.map((plot, index) => (
          <div key={index} className="plot-container">
            <img src={`data:image/png;base64,${plot}`} alt={`Location Plot ${index}`} />
          </div>
        ))}
      </div>
      <h2>To reset and start again click the reset button below </h2>
      <button className="reset-button" onClick={onReset}>Reset</button>
    </div>
  );
};

export default BOResults;
