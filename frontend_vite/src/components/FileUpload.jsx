import React, { useState } from 'react';
import axios from 'axios';
import Spinner from './Spinner';
import InitialEvaluation from './InitialEvaluation';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [showEvaluation, setShowEvaluation] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      console.log('Uploading file with data:', formData);
      const response = await axios.post('http://localhost:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Response:', response);

      setMessage(response.data.status);
      setShowEvaluation(true);
    } catch (error) {
      console.error('File upload failed:', error);
      setMessage('File upload failed');
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluationComplete = () => {
    setShowEvaluation(false);
    setMessage('Evaluation complete');
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload} disabled={loading}>Upload File</button>
      {loading && <Spinner />}
      {message && <p>{message}</p>}
      {showEvaluation && (
        <InitialEvaluation onEvaluationComplete={handleEvaluationComplete} />
      )}
    </div>
  );
};

export default FileUpload;
