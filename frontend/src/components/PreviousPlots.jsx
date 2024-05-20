// src/components/PreviousPlots.jsx
import React from 'react';

const PreviousPlots = ({ plotHistory }) => {
  // Exclude the latest item and reverse the order
  const history = plotHistory.slice(0, -1).reverse();

  return (
    <div>
      <h2>Previous Plots</h2>
      {history.map((item, index) => (
        <div key={index}>
          <img src={`data:image/png;base64,${item.plot_data.plot}`} alt={`Plot ${index}`} style={{ width: '500px'}} />
          <p>Vote: {item.rating?.vote ?? 'N/A'}</p>
          <p>Weight Pref: {item.rating?.newspec_pref ?? 'N/A'}</p>
          <p>Weight: {item.rating?.newspec_wt ?? 'N/A'}</p>
        </div>
      ))}
    </div>
  );
};

export default PreviousPlots;
