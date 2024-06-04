// src/App.jsx
import React, { useState } from 'react';
import NumStartInput from './components/NumStartInput';
import FileUpload from './components/FileUpload';
import EvaluationButton from './components/EvaluationButton';
import PlotDisplay from './components/PlotDisplay';
import VoteInput from './components/VoteInput';
import PreviousPlots from './components/PreviousPlots';
import VotesPage from './components/VotesPage';
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

  const handleNumStartSet = () => {
    setNumStartSet(true);
  };

  const handleFileUploadComplete = () => {
    setPreprocessingDone(true);
  };

  const startEvaluation = async () => {
    try {
      const response = await axios.post('http://localhost:8000/initial_eval_loop_plot/');
      console.log(response.data);
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
      console.log(response.data);
      setCurrentIteration((prev) => prev + 1);
      setPlotHistory(response.data.plot_history);
      if (currentIteration >= numStart) {
        const finishResponse = await axios.post('http://localhost:8000/initial_eval_finish/');
        console.log(finishResponse.data);
        setTrainY(finishResponse.data.train_Y);
        setVotingComplete(true);
      } else {
        const nextResponse = await axios.post('http://localhost:8000/initial_eval_loop_plot/');
        console.log(nextResponse.data);
        setCurrentPlot(nextResponse.data.plot_data);
        setCurrentWcountGood(nextResponse.data.current_wcount_good);
        setPlotHistory(nextResponse.data.plot_history);
      }
    } catch (error) {
      console.error('Error submitting vote:', error);
    }
  };

  if (votingComplete) {
    return <VotesPage plotHistory={plotHistory} trainY={trainY} />;
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
