import numpy as np
import atomai as aoi
from atomai import utils

def preprocess(data):
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

    check1 =  {
        "img_shape": img.shape,
        "vdc_vec_shape": vdc_vec.shape,
        "amp_slices_shape": amp_slices.shape,
        "specim_shape": specim.shape
    }
    
    window_size = 4
    
    coordinates = aoi.utils.get_coord_grid(img, step=1, return_dict=False)
    features, targets, indices = aoi.utils.extract_patches_and_spectra(specim, img, coordinates=coordinates, window_size=window_size, avg_pool=1)

    check2 = {
        "features.shape": features.shape, 
        "targets.shape": targets.shape
        }
    
    norm_ = lambda x: (x - x.min()) / x.ptp()
    features, targets = norm_(features), norm_(targets)
    
    n, d1, d2 = features.shape
    num_start = int(10)
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
    
    check3 = {
        "X_feas_shape": X_feas.shape,
        "X_feas_norm_shape": X_feas_norm.shape,
        "train_X_shape": train_X.shape,
        "train_X_norm_shape": train_X_norm.shape,
        "train_indices_shape": train_indices.shape,
        "amp_masked_shape": amp_masked.shape
    }
    
    return {"checks": {"check1": check1, "check2": check2, "check3": check3}, 
            "idx": idx,
            "train_X": train_X, 
            "train_X_norm": train_X_norm,
            "train_indices": train_indices,
            "amp_masked": amp_masked,
            "spec_length": spec_length,
            "N": N,
            "m": m,
            "n": n,
            "d1": d1,
            "d2": d2,
            "coordinates": coordinates,
            "features": features,
            "targets": targets,
            "vdc_vec": vdc_vec,
            "img": img,
            "amp_slices": amp_slices,
            "specim": specim,
            "amp_mat": amp_mat,
            "amp_slices": amp_slices,
            "vdc_full": vdc_full,
            "window_size": window_size,
            "norm_": norm_}