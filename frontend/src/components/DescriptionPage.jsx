import React from 'react';
import '../styles/DescriptionPage.css';
import problemImage from '../styles/images/fig_software.jpg'; // Import the image

const DescriptionPage = ({ onProceed }) => {
  return (
    <div className="description-container">
      <h1>Problem Description</h1>
      <p className="description-text">
        Build a partial human in the loop BO framework- 
      </p>
      <p className='description-text'>
        Here we have an image data, where X is the input location of the image.
        Each location in the image, we have spectral data, from where user select if the data is good/bad (discrete choices).
        We generate the target spectral to explore from the weighted average of all the user chosen spectral.
      </p>
      <p className="description-text">
        At the mid of execution, the user also has option to either eliminate (or update the preference) all the previously stored 
        (if user suddenly discover a desired spectral) spectral and put more weights on new found spectral.
      </p>
      <p className="description-text">
        The goal is to build an optimization (BO) model where we adaptively sample towards region (in image) of good spectral, and 
        find optimal location point closest to the current chosen target spectral (as per user voting).
      </p>
      <p className="description-text">
        For detail understanding of the workflow, please refer to the
        <a href="https://github.com/your-github-repo" target="_blank" rel="noopener noreferrer" className="github-link"> GitHub repository</a>.
      </p>
      <img src={problemImage} alt="Problem Description" className="description-image" />
      <button className="proceed-button" onClick={onProceed}>Proceed</button>
    </div>
  );
};

export default DescriptionPage;
