# dKLBO_web

MAC_USERS - Refer to the "MAC_Instructions.md"

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
      The below figure is adapted from<sup><a href="https://doi.org/10.1038/s41524-023-01191-5" target="_blank" rel="noopener noreferrer" className="github-link">[1]</a></sup>. Please cite our below paper if you use this tool in your research.
      </p>
      <img src={./frontend/src/styles/images/fig_software.jpg} alt="Problem Description" className="description-image" />
      <button className="proceed-button" onClick={onProceed}>Proceed</button>
      <p className="reference-text"><a href="https://doi.org/10.1038/s41524-023-01191-5" target="_blank" rel="noopener noreferrer" className="github-link"> [1] Biswas, A., Liu, Y., Creange, N. et al. A dynamic Bayesian optimized active recommender system for curiosity-driven partially Human-in-the-loop automated experiments. npj Comput Mater 10, 29 (2024).</a></p>
    </div>
