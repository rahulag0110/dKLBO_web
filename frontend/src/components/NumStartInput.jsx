// src/components/NumStartInput.jsx
import React, { useState } from 'react';
import axios from 'axios';

const NumStartInput = () => {
  const [numStart, setNumStart] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/set_num_start/', { num_start: parseInt(numStart) });
      console.log(response.data);
      alert('Num start set successfully');
    } catch (error) {
      console.error('Error setting num start:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Num Start:
        <input
          type="number"
          value={numStart}
          onChange={(e) => setNumStart(e.target.value)}
        />
      </label>
      <button type="submit">Set Num Start</button>
    </form>
  );
};

export default NumStartInput;
