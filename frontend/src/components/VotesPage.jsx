// src/components/VotesPage.jsx
import React from 'react';

const VotesPage = ({ plotHistory, trainY }) => {
  // Reverse the order of plot history to display the latest first
  const history = plotHistory.reverse();

  return (
    <div>
      <h1>Your Votes</h1>
      <div>
        <h2>Train Y Data</h2>
        <pre>{JSON.stringify(trainY, null, 2)}</pre>
      </div>
      {history.map((item, index) => (
        <div key={index}>
          <img src={`data:image/png;base64,${item.plot_data.plot}`} alt={`Plot ${index}`} style={{ width: '1000px' }}/>
          <p>Vote: {item.rating?.vote ?? 'N/A'}</p>
          <p>Weight Pref: {item.rating?.newspec_pref ?? 'N/A'}</p>
          <p>Weight: {item.rating?.newspec_wt ?? 'N/A'}</p>
        </div>
      ))}
    </div>
  );
};

export default VotesPage;
