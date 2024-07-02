// src/components/EvaluationButton.jsx
import React from 'react';
import '../styles/EvaluationButton.css';  // Importing the specific CSS file for styling

const EvaluationButton = ({ startEvaluation }) => {
  return (
    <div className="evaluation-container">
      {/* <p className="evaluation-description">Description of the evaluation process...</p> */}
      <button onClick={startEvaluation} className="evaluation-button">
        Start Initial Evaluation
      </button>
    </div>
  );
};

export default EvaluationButton;
