// src/components/FileUpload.jsx
import React, { useState } from 'react';
import axios from 'axios';
import LoadingBar from './LoadingBar'; // Ensure this is correctly imported

const FileUpload = ({ onFileUploadComplete }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isUploaded, setIsUploaded] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setIsUploaded(false); // Ensure we reset this state in case of repeated uploads
    let intervalId = null;
    let timeoutId = setTimeout(() => {
      setProgress(90);
      clearInterval(intervalId);
    }, 120000); // Set to reach 90% at 2 minutes

    // Start a timer to increment the progress
    intervalId = setInterval(() => {
      setProgress((prevProgress) => {
        if (prevProgress < 90) {
          return prevProgress + (90 / 120); // Increment such that it reaches 90 in 120 seconds
        }
        clearInterval(intervalId);
        return prevProgress;
      });
    }, 1000); // Update progress every second

    try {
      const response = await axios.post('http://localhost:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data);
      // Clear the initial timeout and interval
      clearTimeout(timeoutId);
      clearInterval(intervalId);

      // Animate to 100% in 5 seconds
      let finalProgress = progress;
      const finalInterval = setInterval(() => {
        if (finalProgress < 100) {
          finalProgress += 2; // This will add 2% every 100 ms, completing the remaining part in about 5 seconds
          setProgress(finalProgress);
        } else {
          clearInterval(finalInterval);
          setIsUploaded(true); // Set upload complete here
          setUploading(false); // End uploading only after animation is complete
          alert('Preprocessing done');
          onFileUploadComplete(); // Proceed to the next page after reaching 100%
        }
      }, 100);
      
    } catch (error) {
      console.error('Error uploading file:', error);
      clearInterval(intervalId);
      clearTimeout(timeoutId);
      setUploading(false);
    }
  };

  if (isUploaded) return null; // This line may be too abrupt if the next component doesn't immediately take over

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
