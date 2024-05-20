// src/App.jsx
import React, { useState } from 'react';
import NumStartInput from './components/NumStartInput';


const App = () => {

  return (
    <div>
      <h1>Bayesian Optimization App</h1>
      <NumStartInput />
    </div>
  );
};

export default App;
