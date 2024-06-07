// src/components/BOSetup.jsx
import React, { useState } from 'react';
import axios from 'axios';

const BOSetup = ({ onSetupComplete }) => {
  const [numBO, setNumBO] = useState('');
  const [isSet, setIsSet] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/set_num_bo/', { num_bo: parseInt(numBO) });
      console.log(response.data);
      alert('Number of BO iterations set successfully');
      setIsSet(true);
      onSetupComplete(parseInt(numBO));
    } catch (error) {
      console.error('Error setting number of BO iterations:', error);
    }
  };

  if (isSet) return null;

  return (
    <div>
      <h1>Bayesian Optimization</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Number of BO iterations:
          <input
            type="number"
            value={numBO}
            onChange={(e) => setNumBO(e.target.value)}
          />
        </label>
        <button type="submit">Set Number of BO Iterations</button>
      </form>
    </div>
  );
};

export default BOSetup;
