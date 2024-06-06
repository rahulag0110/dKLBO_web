// src/components/BOSetup.jsx
import React, { useState } from 'react';
import axios from 'axios';

const BOSetup = ({ onBOSetupComplete }) => {
  const [numBo, setNumBo] = useState('');
  const [isSet, setIsSet] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/set_num_bo/', { num_bo: parseInt(numBo) });
      console.log(response.data);
      alert('Num BO set successfully');
      setIsSet(true);
      onBOSetupComplete();
    } catch (error) {
      console.error('Error setting num BO:', error);
    }
  };

  return (
    <div>
      <h1>Bayesian Optimization Setup</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Num BO:
          <input
            type="number"
            value={numBo}
            onChange={(e) => setNumBo(e.target.value)}
          />
        </label>
        <button type="submit">Start BO</button>
      </form>
    </div>
  );
};

export default BOSetup;
