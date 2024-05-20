// src/App.jsx
import React, { useState } from 'react';
import NumStartInput from './components/NumStartInput';
import FileUpload from './components/FileUpload';
import EvaluationButton from './components/EvaluationButton';

const App = () => {
  const [numStartSet, setNumStartSet] = useState(false);
  const [preprocessingDone, setPreprocessingDone] = useState(false);

  const handleNumStartSet = () => {
    setNumStartSet(true);
  };

  const handleFileUploadComplete = () => {
    setPreprocessingDone(true);
  };

  const startEvaluation = () => {
    console.log('Starting initial evaluation');
    // Call the evaluation endpoint here
  };

  return (
    <div>
      <h1>Bayesian Optimization App</h1>
      {!numStartSet && <NumStartInput onNumStartSet={handleNumStartSet} />}
      {numStartSet && !preprocessingDone && <FileUpload onFileUploadComplete={handleFileUploadComplete} />}
      {preprocessingDone && <EvaluationButton startEvaluation={startEvaluation} />}
    </div>
  );
};

export default App;
