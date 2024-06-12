// src/components/BOResults.jsx
import React from 'react';

const BOResults = ({ optimResults, GPFigures, locationPlots }) => {
  const validGPFigures = GPFigures.filter((figure) => figure !== null);
  const validLocationPlots = locationPlots.filter((plot) => plot !== null);

  return (
    <div>
      <h1>Optimization Results</h1>
      <pre>{JSON.stringify(optimResults, null, 2)}</pre>
      <h2>GP Figures</h2>
      {validGPFigures.map((figure, index) => (
        <div key={index}>
          <img src={`data:image/png;base64,${figure}`} alt={`GP Figure ${index}`} style={{ width: '1000px' }} />
        </div>
      ))}
      <h2>Location Plots</h2>
      {validLocationPlots.map((plot, index) => (
        <div key={index}>
          <img src={`data:image/png;base64,${plot}`} alt={`Location Plot ${index}`} style={{ width: '1000px' }} />
        </div>
      ))}
    </div>
  );
};

export default BOResults;
