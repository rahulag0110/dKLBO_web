// src/App.jsx
import React from 'react';
import FileUpload from './components/FileUpload';
import './css/Spinner.css';

function App() {
  return (
    <div className="App">
      <h1>File Upload and Evaluation</h1>
      <FileUpload />
    </div>
  );
}

export default App;
