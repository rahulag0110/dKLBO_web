import React, { useState } from 'react';
import '../styles/VotesPage.css';

const VotesPage = ({ plotHistory, trainY, onGoForBO }) => {
  const [boStarting, setBoStarting] = useState(false); // State to track BO starting status

  // Reverse the order of plot history to display the latest first
  const history = plotHistory.reverse();

  // Flatten the nested trainY array
  const flattenedTrainY = trainY.flat().map((value, index) => <li key={index}>{value}</li>);

  const handleGoForBO = () => {
    setBoStarting(true);
    onGoForBO();
  };

  return (
    <div className="votes-container">
    <button
        className="votes-button"
        onClick={handleGoForBO}
        disabled={boStarting}
      >
        {boStarting ? 'Starting BO...' : 'Start BO'}
      </button>
      <p className="votes-description">Here is the history of your votes and evaluated values.</p>
      <div className="train-y-data">
        <h2>Initial Evaluated Values</h2>
        <ul>{flattenedTrainY}</ul>
      </div>
      <h2>List of Initial User Votes</h2>
      <div className="plot-history">
        {history.map((item, index) => (
          <div key={index} className="plot-item">
            <img src={`data:image/png;base64,${item.plot_data.plot}`} alt={`Plot ${index}`} style={{ width: '1000px' }}/>
            <p>Vote: {item.rating?.vote ?? 'N/A'}</p>
            {item.rating?.newspec_pref === 1 && (
              <p>Weight: {item.rating?.newspec_wt ?? 'N/A'}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default VotesPage;
