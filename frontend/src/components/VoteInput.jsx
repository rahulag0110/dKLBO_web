// src/components/VoteInput.jsx
import React, { useState, useEffect } from 'react';
import '../styles/InitialEvalVoting.css'; // Ensure the path matches your structure

const VoteInput = ({ onVoteSubmit, currentWcountGood }) => {
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
  }, [currentWcountGood, onVoteSubmit]);

  const handleVoteChange = (event) => {
    const value = parseInt(event.target.value);
    setVote(value);
    if (value > 0 && currentWcountGood > 0) {
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
    if (vote > 0 && currentWcountGood === 0) {
      setNewspecPref(0);
      setNewspecWt(10); // Assuming the maximum weight in this case
    }
    onVoteSubmit({ "vote": vote, "newspec_pref": newspecPref, "newspec_wt": newspecWt});
  };

  return (
    <div className="evaluation-section">
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
            Do you want to specify a weight?:
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
            Weight:
            <input type="range" min="0" max="10" value={newspecWt} onChange={handleWeightChange} />
            {newspecWt}
          </label>
        </div>
      )}
      <br />
      <button onClick={handleSubmit} className="evaluation-button">Submit Vote</button>
    </div>
  );
};

export default VoteInput;
