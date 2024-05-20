// src/components/NumStartInput.jsx
import React, { useState } from 'react';
import axios from 'axios';

const NumStartInput = ({ onNumStartSet }) => {
  const [numStart, setNumStart] = useState('');
  const [isSet, setIsSet] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/set_num_start/', { num_start: parseInt(numStart) });
      console.log(response.data);
      alert('Num start set successfully');
      setIsSet(true);
      onNumStartSet();
    } catch (error) {
      console.error('Error setting num start:', error);
    }
  };

  if (isSet) return null;

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
