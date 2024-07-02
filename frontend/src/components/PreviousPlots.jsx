// src/components/PreviousPlots.jsx
import React from 'react';
import '../styles/InitialEvalVoting.css'; // Ensure the path matches your structure

const PreviousPlots = ({ plotHistory }) => {
  // Exclude the latest item and reverse the order
  const history = plotHistory.slice(0, -1).reverse();

  return (
    <div className="evaluation-section">
      <h2>Previous plots</h2>
      {history.map((item, index) => (
        <div key={index}>
          <img src={`data:image/png;base64,${item.plot_data.plot}`} alt={`Plot ${index}`} style={{ width: '500px'}} />
          <p>Vote: {item.rating?.vote ?? 'N/A'}</p>
          {item.rating?.newspec_pref === 1 && (
              <p>Weight: {item.rating?.newspec_wt ?? 'N/A'}</p>
            )}
        </div>
      ))}
    </div>
  );
};

export default PreviousPlots;
