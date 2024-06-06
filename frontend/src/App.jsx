// src/App.jsx
import React, { useState } from 'react';
import NumStartInput from './components/NumStartInput';
import FileUpload from './components/FileUpload';
import EvaluationButton from './components/EvaluationButton';
import PlotDisplay from './components/PlotDisplay';
import VoteInput from './components/VoteInput';
import PreviousPlots from './components/PreviousPlots';
import VotesPage from './components/VotesPage';
import BOSetup from './components/BOSetup';
import axios from 'axios';

const App = () => {
  const [numStartSet, setNumStartSet] = useState(false);
  const [preprocessingDone, setPreprocessingDone] = useState(false);
  const [currentPlot, setCurrentPlot] = useState(null);
  const [currentWcountGood, setCurrentWcountGood] = useState(0);
  const [plotHistory, setPlotHistory] = useState([]);
  const [currentIteration, setCurrentIteration] = useState(0);
  const [numStart, setNumStart] = useState(0);
  const [initialEvalStarted, setInitialEvalStarted] = useState(false);
  const [votingComplete, setVotingComplete] = useState(false);
  const [trainY, setTrainY] = useState(null);
  const [boSetup, setBOSetup] = useState(false);

  const handleNumStartSet = () => {
    setNumStartSet(true);
  };

  const handleFileUploadComplete = () => {
    setPreprocessingDone(true);
  };

  const startEvaluation = async () => {
    try {
      const response = await axios.post('http://localhost:8000/initial_eval_loop_plot/');
      setCurrentPlot(response.data.plot_data);
      setCurrentWcountGood(response.data.current_wcount_good);
      setPlotHistory(response.data.plot_history);
      setCurrentIteration(1);
      setNumStart(response.data.num_start); // Assuming the backend can return num_start
      setInitialEvalStarted(true);
    } catch (error) {
      console.error('Error fetching initial plot:', error);
    }
  };

  const handleVoteSubmit = async (voteData) => {
    try {
      const response = await axios.post('http://localhost:8000/initial_eval_vote_process/', voteData);
      setCurrentIteration((prev) => prev + 1);
      setPlotHistory(response.data.plot_history);
      if (currentIteration + 1 >= numStart) {
        const finishResponse = await axios.post('http://localhost:8000/initial_eval_finish');
        setTrainY(finishResponse.data.train_Y);
        setVotingComplete(true);
      } else {
        const nextResponse = await axios.post('http://localhost:8000/initial_eval_loop_plot/');
        setCurrentPlot(nextResponse.data.plot_data);
        setCurrentWcountGood(nextResponse.data.current_wcount_good);
        setPlotHistory(nextResponse.data.plot_history);
      }
    } catch (error) {
      console.error('Error submitting vote:', error);
    }
  };

  const handleGoForBO = async () => {
    try {
      await axios.post('http://localhost:8000/bo_setup/');
      setBOSetup(true);
    } catch (error) {
      console.error('Error setting up BO:', error);
    }
  };

  const handleBOSetupComplete = () => {
    // Handle the next steps after setting num_bo, e.g., transition to the BO process page
    console.log('BO setup complete');
  };

  if (boSetup) {
    return <BOSetup onBOSetupComplete={handleBOSetupComplete} />;
  }

  if (votingComplete) {
    return <VotesPage plotHistory={plotHistory} trainY={trainY} onGoForBO={handleGoForBO} />;
  }

  return (
    <div>
      <h1>Bayesian Optimization App</h1>
      {!numStartSet && <NumStartInput onNumStartSet={handleNumStartSet} />}
      {numStartSet && !preprocessingDone && <FileUpload onFileUploadComplete={handleFileUploadComplete} />}
      {preprocessingDone && <EvaluationButton startEvaluation={startEvaluation} />}
      {currentPlot && (
        <div>
          <PlotDisplay plotData={currentPlot} />
          <VoteInput onVoteSubmit={handleVoteSubmit} currentWcountGood={currentWcountGood} />
        </div>
      )}
      {initialEvalStarted && <PreviousPlots plotHistory={plotHistory} />}
    </div>
  );
};

export default App;
