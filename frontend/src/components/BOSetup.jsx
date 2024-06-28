import React, { useState } from 'react';
import axios from 'axios';
import '../styles/BOSetup.css';

const BOSetup = ({ onSetupComplete, onStartBOLoop }) => {
  const [numBO, setNumBO] = useState('');
  const [isSet, setIsSet] = useState(false);
  const [isStarting, setIsStarting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/set_num_bo/', { num_bo: parseInt(numBO) });
      console.log(response.data);
      setIsSet(true);
      onSetupComplete(parseInt(numBO));
      handleStartBOLoop();
    } catch (error) {
      console.error('Error setting number of BO iterations:', error);
    }
  };

  const handleStartBOLoop = async () => {
    setIsStarting(true);
    await onStartBOLoop();
    setIsStarting(false);
  };

  if (isSet && !isStarting) return null;

  return (
    <div className="bo-setup-container">
      <p className="description">Description...</p>
      <form onSubmit={handleSubmit} className="bo-setup-form">
        <label>
          Number of BO iterations:
          <input
            type="number"
            value={numBO}
            onChange={(e) => setNumBO(e.target.value)}
            placeholder="Enter number of BO iterations"
          />
        </label>
        <button type="submit" className="bo-setup-button" disabled={isStarting}>
            {isStarting ? 'Starting BO Loop...' : 'Click to enter'}
        </button>
      </form>
    </div>
  );
};

export default BOSetup;
