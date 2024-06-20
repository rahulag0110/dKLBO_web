// src/components/FileUpload.jsx
import React, { useState, useRef } from 'react';
import axios from 'axios';
import LoadingBar from './LoadingBar'; // Ensure this is correctly imported

const FileUpload = ({ onFileUploadComplete }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const progressRef = useRef(progress); // Use useRef to track the current progress

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    progressRef.current = 0; // Reset progress ref
    setProgress(0); // Reset progress state

    let intervalId = setInterval(() => {
      if (progressRef.current < 90) {
        progressRef.current += 4.3; // Increment by 1.5% every second to reach 90% in 120 seconds
        setProgress(progressRef.current);
      } else {
        clearInterval(intervalId);
      }
    }, 1000);

    try {
      const response = await axios.post('http://localhost:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data);
      clearInterval(intervalId);

      // Animate to 100% in 5 seconds
      let step = (100 - progressRef.current) / 50; // Calculate steps to reach 100 in 5 seconds
      const finalInterval = setInterval(() => {
        if (progressRef.current < 100) {
          progressRef.current += step;
          if (progressRef.current > 100) {
            progressRef.current = 100; // Ensure it reaches 100
          }
          setProgress(progressRef.current);
        } else {
          clearInterval(finalInterval);
          setProgress(100); // Ensure it reaches 100
          setUploading(false); // End uploading
          alert('File uploaded successfully!');
          onFileUploadComplete(); // Callback to parent to proceed
        }
      }, 100);

    } catch (error) {
      console.error('Error uploading file:', error);
      clearInterval(intervalId);
      setUploading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={!file || uploading}>
        {uploading ? <LoadingBar progress={progress} /> : 'Upload File'}
      </button>
    </div>
  );
};

export default FileUpload;
