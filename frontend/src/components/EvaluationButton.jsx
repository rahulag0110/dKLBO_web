// src/components/EvaluationButton.jsx
import React from 'react';

const EvaluationButton = ({ startEvaluation }) => {
  return (
    <button onClick={startEvaluation}>
      Start Initial Evaluation
    </button>
  );
};

export default EvaluationButton;
