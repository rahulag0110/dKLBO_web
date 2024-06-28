// src/App.jsx
import React, { useState } from 'react';
import FileNumStartUpload from './components/FileNumStartUpload';
import EvaluationButton from './components/EvaluationButton';
import PlotDisplay from './components/PlotDisplay';
import VoteInput from './components/VoteInput';
import PreviousPlots from './components/PreviousPlots';
import VotesPage from './components/VotesPage';
import BOSetup from './components/BOSetup';
import BOPlotsDisplay from './components/BOPlotsDisplay';
import BOResults from './components/BOResults'; // Import new component
import BOUnsatisfiedVote from './components/BOUnsatisfiedVote'; // Import new component
import axios from 'axios';
import LoadingBar from './components/LoadingBar';

import './styles/Global.css';

const App = () => {
  // Initial Evaluation Checkpoint Variables
  const [numStartSet, setNumStartSet] = useState(false);
  const [preprocessingDone, setPreprocessingDone] = useState(false);
  const [initialEvalStarted, setInitialEvalStarted] = useState(false);
  const [votingComplete, setVotingComplete] = useState(false);

  // Initial Evaluation Data Variables
  const [currentPlot, setCurrentPlot] = useState(null);
  const [currentWcountGood, setCurrentWcountGood] = useState(0);
  const [plotHistory, setPlotHistory] = useState([]);
  const [currentIteration, setCurrentIteration] = useState(0);
  const [numStart, setNumStart] = useState(0);
  const [trainY, setTrainY] = useState(null);

  // Bayesian Optimization Checkpoint Variables
  const [boSetup, setBOSetup] = useState(false);
  const [boReady, setBOReady] = useState(false);
  const [boLoopStarted, setBOLoopStarted] = useState(false);
  const [boPlotsReady, setBOPlotsReady] = useState(false);
  const [boLoopFinish, setBOLoopFinish] = useState(false);
  const [boResultsReady, setBOResultsReady] = useState(false); // New state for BO results
  const [unsatisfiedVoteReady, setUnsatisfiedVoteReady] = useState(false); // State for unsatisfied vote

  // Bayesian Optimization Data Variables
  const [numBO, setNumBO] = useState(0);
  const [boPlots, setBOPlots] = useState([]); // State for storing BO plots
  const [boLoopCounter, setBOLoopCounter] = useState(0); // State for BO loop counter
  const [userSatisfied, setUserSatisfied] = useState(null); // State for user satisfaction
  const [GPFigures, setGPFigures] = useState([]); // State for storing GP figures
  const [locationPlots, setLocationPlots] = useState([]); // State for storing location plots
  const [optimResults, setOptimResults] = useState([]); // State for storing optimization results
  const [unsatisfiedPlot, setUnsatisfiedPlot] = useState(null); // State for storing the plot for unsatisfied case


  const [loadingProgress, setLoadingProgress] = useState(0);
  const [loadingVisible, setLoadingVisible] = useState(false);

  // Initial Evaluation Functions
  const handleUploadComplete = () => {
    setNumStartSet(true);
    setPreprocessingDone(true);
  };

  const startEvaluation = async () => {
    try {
      const response = await axios.post('http://localhost:8000/initial_eval_loop_plot/');
      setCurrentPlot(response.data.plot_data);
      setCurrentWcountGood(response.data.current_wcount_good);
      setPlotHistory(response.data.plot_history);
      setCurrentIteration(1);
      setNumStart(response.data.num_start);
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
      if (currentIteration + 1 > numStart) {
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

  // Bayesian Optimization Functions
  const handleGoForBO = async () => {
    try {
      await axios.post('http://localhost:8000/bo_setup/');
      setBOSetup(true);
    } catch (error) {
      console.error('Error setting up BO:', error);
    }
  };

  const handleBOSetupComplete = (numBO) => {
    setNumBO(numBO);
    setBOReady(true);
  };

  const handleStartBOLoop = async () => {
    setBOLoopStarted(true); // Set state to show running message
    try {
      // First Step
      const firstStepResponse = await axios.post('http://localhost:8000/bo_loop_first_step/');
      setBOLoopCounter(firstStepResponse.data.bo_loop_counter);
      setBOPlots(firstStepResponse.data.bo_plots);

      // Second Step
      await axios.post('http://localhost:8000/bo_loop_second_step/');

      // Third Step
      await axios.post('http://localhost:8000/bo_loop_third_step/');

      // Set state to display BO plots
      setBOPlotsReady(true);

    } catch (error) {
      console.error('Error starting BO loop:', error);
    }
  };
  const runAutomatedBOLoop = async () => {
    try {
      // Automated Step
      setLoadingVisible(true);
      const response = await axios.post('http://localhost:8000/bo_loop_automated/');
      setBOLoopCounter(response.data.bo_loop_counter);
      
      if (response.data.bo_loop_counter >= numBO) {
        // Finish BO loop
        setBOLoopFinish(true);
        setLoadingVisible(false);
        setGPFigures(response.data.GP_figures);
        setLocationPlots(response.data.location_plots);

        // Call BO finish endpoint
        const finishResponse = await axios.post('http://localhost:8000/bo_finish/');
        setOptimResults(finishResponse.data.optim_results);
        setBOResultsReady(true);
      } else {
        // Show loading bar
        setLoadingVisible(true);
        runAutomatedBOLoop();
      }
    } catch (error) {
      console.error('Error running automated BO loop:', error);
    }
  };
  const handleUserSatisfactionSubmit = async (satisfaction) => {
    setUserSatisfied(satisfaction);
    console.log(`User satisfaction: ${satisfaction}`);
    setBOPlotsReady(false);
    if (satisfaction) { // If user is satisfied
      try {
        // Fourth Step
        await axios.post('http://localhost:8000/bo_loop_fourth_step_satisfied/');
        
        // Fifth Step
        await axios.post('http://localhost:8000/bo_loop_fifth_step/');
        
        // Show message

        runAutomatedBOLoop();
      } catch (error) {
        console.error('Error completing BO loop:', error);
      }
    } else { // If user is not satisfied
      try {
        // Fourth Step Unsatisfied Plot
        const unsatisfiedPlotResponse = await axios.post('http://localhost:8000/bo_loop_fourth_step_unsatisfied_plot/');
        setUnsatisfiedPlot(unsatisfiedPlotResponse.data.plot);

        // Prepare to vote on the new plot
        setUnsatisfiedVoteReady(true);
        
      } catch (error) {
        console.error('Error handling unsatisfied case:', error);
      }
    }
  };

  const handleUnsatisfiedVoteSubmit = async (voteData) => {
    try {
      // Submit unsatisfied vote
      setUnsatisfiedVoteReady(false);
      await axios.post('http://localhost:8000/bo_loop_fourth_step_unsatisfied_vote_process/', voteData);

      // Fourth Step Unsatisfied
      await axios.post('http://localhost:8000/bo_loop_fourth_step_unsatisfied/');

      // Fifth Step
      const fifthStepResponse = await axios.post('http://localhost:8000/bo_loop_fifth_step/');
      setBOLoopCounter(fifthStepResponse.data.bo_loop_counter);

      if (fifthStepResponse.data.bo_loop_counter > numBO) {
        // Call BO finish endpoint
        const finishResponse = await axios.post('http://localhost:8000/bo_finish/');
        setOptimResults(finishResponse.data.optim_results);
        setBOResultsReady(true);
      } else {
        // Restart BO loop
        handleStartBOLoop();
      }
    } catch (error) {
      console.error('Error submitting unsatisfied vote:', error);
    }
  };

  // Render Logic
  if (boResultsReady) {
    return <BOResults optimResults={optimResults} GPFigures={GPFigures} locationPlots={locationPlots} />; // Render the final results and figures
  }

  if (unsatisfiedVoteReady) {
    return <BOUnsatisfiedVote plotData={unsatisfiedPlot} onVoteSubmit={handleUnsatisfiedVoteSubmit} />; // Render the unsatisfied vote page
  }

  if (boLoopFinish) {
    return <div>Automated BO Completed.</div>; // Placeholder message for automated BO completion
  }

  if (boPlotsReady) {
    return <BOPlotsDisplay boPlots={boPlots} onSatisfactionSubmit={handleUserSatisfactionSubmit} />; // Pass the satisfaction submit handler
  }

  if (boLoopStarted) {
    return (
      <div>
        {/* <div>STEP: {boLoopCounter}/{numBO}</div> */}
        {loadingVisible && <LoadingBar progress={(boLoopCounter / numBO) * 100} />}
      </div>
    );
  }

  if (boSetup) {
    return <BOSetup onSetupComplete={handleBOSetupComplete} onStartBOLoop={handleStartBOLoop} />;
  }

  if (votingComplete) {
    return (
        <>
        <div className="app-container">
            <header>
                <h1>BOARS: Bayesian Optimized Active Recommender System</h1>
                <p className="app-subtitle">A partial human interacted BO framework for autonomous experiments.</p>
            </header>
        </div>
            <VotesPage plotHistory={plotHistory} trainY={trainY} onGoForBO={handleGoForBO} />
        </>
    )
    
  }

  return (
    <div className="app-container">
      <header>
        <h1>BOARS: Bayesian Optimized Active Recommender System</h1>
        <p className="app-subtitle">A partial human interacted BO framework for autonomous experiments.</p>
      </header>
      {!numStartSet && <FileNumStartUpload onUploadComplete={handleUploadComplete} />}
      {preprocessingDone && !initialEvalStarted && <EvaluationButton startEvaluation={startEvaluation} />}
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
