// src/components/VoteInput.jsx
import React, { useState } from 'react';

const VoteInput = ({ onVoteSubmit }) => {
  const [vote, setVote] = useState(0);
  const [newspecPref, setNewspecPref] = useState(-1);
  const [newspecWt, setNewspecWt] = useState(0);

  const handleSubmit = () => {
    onVoteSubmit({ "vote": vote, "newspec_pref": newspecPref, "newspec_wt": newspecWt});
  };

  return (
    <div>
      <label>
        Vote:
        <input
          type="radio"
          name="vote"
          value="0"
          checked={vote === 0}
          onChange={(e) => setVote(parseInt(e.target.value))}
        /> 0
        <input
          type="radio"
          name="vote"
          value="1"
          checked={vote === 1}
          onChange={(e) => setVote(parseInt(e.target.value))}
        /> 1
        <input
          type="radio"
          name="vote"
          value="2"
          checked={vote === 2}
          onChange={(e) => setVote(parseInt(e.target.value))}
        /> 2
      </label>
      <br />
      <label>
        Newspec Pref:
        <input
          type="number"
          value={newspecPref}
          onChange={(e) => setNewspecPref(parseInt(e.target.value))}
        />
      </label>
      <br />
      <label>
        Newspec Wt:
        <input
          type="number"
          value={newspecWt}
          onChange={(e) => setNewspecWt(parseInt(e.target.value))}
        />
      </label>
      <br />
      <button onClick={handleSubmit}>Submit Vote</button>
    </div>
  );
};

export default VoteInput;
