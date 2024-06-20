// src/components/LoadingBar.jsx
import React from 'react';

const LoadingBar = ({ progress }) => {
  const barStyle = {
    width: `${progress}%`,
    backgroundColor: 'blue',
    height: '20px'
  };

  return (
    <div>
      <div style={{ width: '100%', backgroundColor: 'lightgray', height: '20px' }}>
        <div style={barStyle}></div>
      </div>
      <div>{progress.toFixed(0)}%</div>
    </div>
  );
};

export default LoadingBar;
