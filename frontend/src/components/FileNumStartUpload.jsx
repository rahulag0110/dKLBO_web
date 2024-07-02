// src/components/FileNumStartUpload.jsx
import React, { useState, useRef } from 'react';
import axios from 'axios';
import LoadingBar from './LoadingBar';
import '../styles/FileNumStartUpload.css'

const FileNumStartUpload = ({ onUploadComplete}) => {
    
    

    const [file, setFile] = useState(null);
    const [numStart, setNumStart] = useState('');
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);
    const progressRef = useRef(progress);

    const handleNumStartChange = (e) => {
        setNumStart(e.target.value);
    };

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        setUploading(true);
        progressRef.current = 0;
        setProgress(0);

        // First set num_start
        try {
            await axios.post('http://localhost:8000/set_num_start/', { num_start: parseInt(numStart) });
            console.log('Num start set successfully');
        } catch (error) {
            console.error('Error setting num start:', error);
            setUploading(false);
            return;
        }

        // Then upload the file
        const formData = new FormData();
        formData.append('file', file);

        let intervalId = setInterval(() => {
            if (progressRef.current < 90) {
                progressRef.current += 1.5; 
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

            let step = (100 - progressRef.current) / 50;
            const finalInterval = setInterval(() => {
                if (progressRef.current < 100) {
                    progressRef.current += step;
                    if (progressRef.current > 100) {
                        progressRef.current = 100; // Ensure it reaches 100
                    }
                    setProgress(progressRef.current);
                } else {
                    clearInterval(finalInterval);
                    setProgress(100);
                    setUploading(false);
                    onUploadComplete(); // Callback to transition to the next page
                }
            }, 100);
        } catch (error) {
            console.error('Error uploading file:', error);
            clearInterval(intervalId);
            setUploading(false);
        }
    };

    return (
        <div className="upload-container">
            <p className="description">Provide data and number of initial assessments</p>
            <input type="file" onChange={handleFileChange} />
            <span className="file-name">{file ? file.name : 'No file chosen'}</span>
            <input
                type="number"
                value={numStart}
                onChange={handleNumStartChange}
                placeholder="Number of initial (random) evaluations"
            />
            <button onClick={handleUpload} disabled={!file || !numStart || uploading}>
                {uploading ? <LoadingBar progress={progress} /> : 'Initialize BO'}
            </button>
        </div>
    );
};

export default FileNumStartUpload;