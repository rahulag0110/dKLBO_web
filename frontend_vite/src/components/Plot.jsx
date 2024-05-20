// src/Plot.jsx
import React, { useState, useEffect } from 'react';

const Plot = ({ plotData, onVoteSubmit, voteCount, title, currentWcountGood }) => {
  const [vote, setVote] = useState(null);
  const [newspecPref, setNewspecPref] = useState(1);
  const [newspecWt, setNewspecWt] = useState(1);

  useEffect(() => {
    setVote(null); // Reset the vote state when plotData changes
    setNewspecPref(1); // Reset the newspecPref state when plotData changes
    setNewspecWt(1); // Reset the newspecWt state when plotData changes
  }, [plotData]);

  const handleVoteChange = (e) => {
    setVote(parseInt(e.target.value));
    if (parseInt(e.target.value) === 0) {
      setNewspecPref(null);
      setNewspecWt(1);
    }
  };

  const handlePrefChange = (e) => {
    setNewspecPref(parseInt(e.target.value));
  };

  const handleWtChange = (e) => {
    setNewspecWt(parseInt(e.target.value) / 10);
  };

  const handleSubmit = async () => {
    if (vote !== null) {
      const rating = {
        vote: vote,
        newspec_pref: newspecPref,
        newspec_wt: newspecWt,
      };

      await onVoteSubmit(rating);
    }
  };

  return (
    <div>
      {title && <h3>{title}</h3>}
      <img src={`data:image/png;base64,${plotData}`} alt="Plot" style={{ width: '1000px'}} />
      <div>
        <label>
          <input type="radio" value={0} checked={vote === 0} onChange={handleVoteChange} /> 0
        </label>
        <label>
          <input type="radio" value={1} checked={vote === 1} onChange={handleVoteChange} /> 1
        </label>
        <label>
          <input type="radio" value={2} checked={vote === 2} onChange={handleVoteChange} /> 2
        </label>
      </div>
      {currentWcountGood > 0 && vote > 0 && (
        <div>
          <p>Do you want to update preference to new spectral over prior mean target?</p>
          <label>
            <input type="radio" value={1} checked={newspecPref === 1} onChange={handlePrefChange} /> Yes
          </label>
          <label>
            <input type="radio" value={0} checked={newspecPref === 0} onChange={handlePrefChange} /> No
          </label>
        </div>
      )}
      {newspecPref === 1 && (
        <div>
          <p>Provide weights between 0 and 10:</p>
          <input
            type="range"
            min="0"
            max="10"
            value={newspecWt * 10}
            onChange={handleWtChange}
          />
          <p>Weight: {newspecWt * 10}</p>
        </div>
      )}
      <button onClick={handleSubmit}>Submit Vote</button>
    </div>
  );
};

export default Plot;
