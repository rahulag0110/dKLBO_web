// src/components/BOUnsatisfiedVote.jsx
import React, { useState, useEffect } from 'react';
import '../styles/BOUnsatisfiedVote.css';

const BOUnsatisfiedVote = ({ plotData, onVoteSubmit }) => {
  const [vote, setVote] = useState(0);
  const [showPrefOption, setShowPrefOption] = useState(false);
  const [newspecPref, setNewspecPref] = useState(0);
  const [newspecWt, setNewspecWt] = useState(0);
  const [showWeightOption, setShowWeightOption] = useState(false);

  useEffect(() => {
    setVote(0);
    setShowPrefOption(false);
    setNewspecPref(0);
    setNewspecWt(0);
    setShowWeightOption(false);
  }, [plotData]);

  const handleVoteChange = (event) => {
    const value = parseInt(event.target.value);
    setVote(value);
    if (value > 0) {
      setShowPrefOption(true);
    } else {
      setShowPrefOption(false);
      setShowWeightOption(false);
    }
  };

  const handlePrefChange = (event) => {
    const value = parseInt(event.target.value);
    setNewspecPref(value);
    if (value === 1) {
      setShowWeightOption(true);
    } else {
      setShowWeightOption(false);
    }
  };

  const handleWeightChange = (event) => {
    setNewspecWt(parseInt(event.target.value));
  };

  const handleSubmit = () => {
    onVoteSubmit({ "vote": vote, "newspec_pref": newspecPref, "newspec_wt": newspecWt });
  };

  return (
    <div className="evaluation-section">
      <h2>Unsatisfied BO Vote</h2>
      <img src={`data:image/png;base64,${plotData}`} alt="Unsatisfied Plot" />
    <label>
      Vote:
        <input
          type="radio"
          name="vote"
          value="0"
          checked={vote === 0}
          onChange={handleVoteChange}
        /> 0
        <input
          type="radio"
          name="vote"
          value="1"
          checked={vote === 1}
          onChange={handleVoteChange}
        /> 1
        <input
          type="radio"
          name="vote"
          value="2"
          checked={vote === 2}
          onChange={handleVoteChange}
        /> 2
      </label>
      <br />
      {showPrefOption && (
        <div>
          <label>
            New Spec Pref:
            <input
              type="radio"
              name="newspecPref"
              value="0"
              checked={newspecPref === 0}
              onChange={handlePrefChange}
            /> No
            <input
              type="radio"
              name="newspecPref"
              value="1"
              checked={newspecPref === 1}
              onChange={handlePrefChange}
            /> Yes
          </label>
          <br />
        </div>
      )}
      {showWeightOption && (
        <div>
          <label>
            New Spec Weight:
            <input type="range" min="0" max="10" value={newspecWt} onChange={handleWeightChange} />
            {newspecWt}
          </label>
        </div>
      )}
      <button className="evaluation-button" onClick={handleSubmit}>Submit Vote</button>
    </div>
  );
};

export default BOUnsatisfiedVote;
