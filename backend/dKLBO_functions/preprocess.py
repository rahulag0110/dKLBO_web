import numpy as np
import atomai as aoi
from atomai import utils

def preprocess(data, num_start):
    # Extract BEPS data
    beps_all = data['results_beps']
    
    spec_length = 64 
    amp_slices = [beps_all[ind][1][2] for ind in range(len(beps_all))]
    amp_slices = np.array(amp_slices)
    img = amp_slices[:, 16].reshape(50, 50)

    vdc_full = np.array(beps_all[0][1][0])
    vdc_vec = vdc_full[-64:]

    amp_mat = amp_slices[:, -128:][:, 1::2]
    amp_masked = np.zeros_like(amp_mat)

    spec_length = amp_mat.shape[-1]  # Update spectral data length
    specim = np.reshape(amp_mat, (img.shape[0], img.shape[1], spec_length))

    # check1 =  {
    #     "img_shape": img.shape,
    #     "vdc_vec_shape": vdc_vec.shape,
    #     "amp_slices_shape": amp_slices.shape,
    #     "specim_shape": specim.shape
    # }
    
    window_size = 4
    
    coordinates = aoi.utils.get_coord_grid(img, step=1, return_dict=False)
    features, targets, indices = aoi.utils.extract_patches_and_spectra(specim, img, coordinates=coordinates, window_size=window_size, avg_pool=1)

    # check2 = {
    #     "features.shape": features.shape, 
    #     "targets.shape": targets.shape
    #     }
    
    norm_ = lambda x: (x - x.min()) / x.ptp()
    features, targets = norm_(features), norm_(targets)
    
    n, d1, d2 = features.shape
    N = int(100)
    m = 0
    spec_length = amp_mat.shape[-1]  #spectral data length

    coordinates = utils.get_coord_grid(img, 1)
    X_feas = features.reshape(n, d1*d2)

    X_feas_norm = features.reshape(n, d1*d2)

    amp_masked = np.zeros_like(targets)
    np.random.seed(10)

    idx = np.random.randint(0, len(X_feas), num_start)
    for ind in range(num_start):
        amp_masked[int(idx[ind]),:] = targets[int(idx[ind]),:]

    train_X = X_feas[idx]
    train_X_norm = X_feas_norm[idx]
    train_indices = indices[idx]
    
    # check3 = {
    #     "X_feas_shape": X_feas.shape,
    #     "X_feas_norm_shape": X_feas_norm.shape,
    #     "train_X_shape": train_X.shape,
    #     "train_X_norm_shape": train_X_norm.shape,
    #     "train_indices_shape": train_indices.shape,
    #     "amp_masked_shape": amp_masked.shape
    # }
    
    IV = np.copy(amp_masked)
    points_measured = np.array(idx)
    last_points_measured = np.array(points_measured)
    vdc = vdc_vec
    
    train_Y = np.zeros((num_start, 1))
    pref = np.zeros((num_start, 1))
    init_spec = np.zeros((num_start, spec_length))
    # Define a sparse grid to store evaluated spectral locations
    eval_spec_y = np.zeros((img.shape[0],img.shape[0],spec_length))
    #Evaluate initial training data
    x = np.zeros((1,2))
    
    # First generate target loop, based on initial training data
    wcount_good= 0
    target_func = np.zeros(spec_length)
    
    mask = np.isin(points_measured, last_points_measured, invert = True)
    new_points_measured = points_measured[mask]
    last_points_measured = np.append(last_points_measured, new_points_measured)

    initial_eval_loop_counter = 0
    
    return { 
            "amp_masked": amp_masked,
            "idx": idx,
            "vdc_vec": vdc_vec,
            "num_start": num_start,
            "img": img,
            "spec_length": spec_length,
            "X_feas": X_feas,
            "X_feas_norm": X_feas_norm,
            "train_X": train_X,
            "train_X_norm": train_X_norm,
            "train_indices": train_indices,
            "m": m,
            "points_measured": points_measured,
            "last_points_measured": last_points_measured,
            "IV": IV,
            "init_spec": init_spec,
            "eval_spec_y": eval_spec_y,
            "train_Y": train_Y,
            "pref": pref,
            "wcount_good": wcount_good,
            "target_func": target_func,
            "initial_eval_loop_counter": initial_eval_loop_counter
            }