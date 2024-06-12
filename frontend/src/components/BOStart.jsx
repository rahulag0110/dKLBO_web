// src/components/BOStart.jsx
import React from 'react';

const BOStart = ({ onStartBOLoop }) => {
  return (
    <div>
      <h1>Bayesian Optimization Loop</h1>
      <button onClick={onStartBOLoop}>Start BO Loop</button>
    </div>
  );
};

export default BOStart;
