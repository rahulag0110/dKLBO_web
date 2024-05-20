import React, { useState } from 'react';
import axios from 'axios';
import Plot from './Plot';

const InitialEvaluation = ({ onEvaluationComplete }) => {
  const [plotData, setPlotData] = useState(null);
  const [plotHistory, setPlotHistory] = useState([]);
  const [voteCount, setVoteCount] = useState(0);
  const [message, setMessage] = useState('');
  const [currentWcountGood, setCurrentWcountGood] = useState(0);

  const handleInitialEvaluation = async () => {
    try {
      console.log('Calling /initial_eval_loop_plot/ endpoint');
      const response = await axios.post('http://localhost:8000/initial_eval_loop_plot/');
      console.log('Response:', response);

      setPlotData(response.data.plot_data.plot);
      setCurrentWcountGood(response.data.current_wcount_good);
      setVoteCount(0);
      setPlotHistory([]);
      setMessage('');
    } catch (error) {
      console.error('Error starting initial evaluation:', error);
    }
  };

  const handleVoteSubmit = async (rating) => {
    try {
      console.log('Submitting vote with data:', rating);
      const response = await axios.post('http://localhost:8000/initial_eval_vote_process/', rating);
      console.log('Response:', response);

      setVoteCount((prevCount) => prevCount + 1);
      setPlotHistory((prevHistory) => [...prevHistory, { plotData, rating }]);

      if (voteCount < 9) {
        // Get the next plot data
        const newResponse = await axios.post('http://localhost:8000/initial_eval_loop_plot/');
        console.log('Response:', newResponse);
        setPlotData(newResponse.data.plot_data.plot);
        setCurrentWcountGood(newResponse.data.current_wcount_good);
      } else {
        setMessage('Evaluation complete');
        onEvaluationComplete();
      }
    } catch (error) {
      console.error('Error processing vote:', error);
    }
  };

  return (
    <div>
      <button onClick={handleInitialEvaluation}>
        Start Initial Evaluation
      </button>
      {plotData && (
        <Plot
          plotData={plotData}
          onVoteSubmit={handleVoteSubmit}
          voteCount={voteCount}
          title={`Plot No. ${voteCount + 1}`}
          currentWcountGood={currentWcountGood}
        />
      )}
      <div>
        <h2>Plot History</h2>
        {plotHistory.map((plot, index) => (
          <div key={index} style={{ marginBottom: '20px' }}>
            <h3>Plot No. {index + 1} [Vote: {plot.rating.vote}]</h3>
            <img src={`data:image/png;base64,${plot.plotData}`} alt={`Plot ${index + 1}`} style={{ width: '500px' }} />
            {plot.rating.vote > 0 && (
              <p>newspec_pref: {plot.rating.newspec_pref}, newspec_wt: {plot.rating.newspec_wt}</p>
            )}
          </div>
        ))}
      </div>
      {message && <p>{message}</p>}
    </div>
  );
};

export default InitialEvaluation;
