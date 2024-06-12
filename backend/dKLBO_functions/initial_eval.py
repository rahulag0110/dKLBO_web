import numpy as np
import matplotlib.pyplot as plt
import base64
import io
from skimage.metrics import structural_similarity as ssim

def generate_plots_for_initial_eval(idx_x, idx_y, new_spec_x, new_spec_y, img, wcount_good, target_func):
    #parameters_needed = idx_x, idx_y, new_spec_x, new_spec_y, img, wcount_good, target_func
    idx1 = int(idx_x)
    idx2 = int(idx_y)
    plot_data = {}
    
    if (wcount_good == 0):
        # Figure for user choice
        fig,ax=plt.subplots(ncols=2,figsize=(12,5))
        ax[0].imshow(img, origin="lower")
        ax[0].scatter(idx2, idx1, marker = 'x', color="red")
        ax[0].axes.xaxis.set_visible(False)
        ax[0].axes.yaxis.set_visible(False)
        ax[1].plot(new_spec_x, new_spec_y)
        ax[1].set_title('loc:' +str(idx2) +"," + str(idx1), fontsize = 20)
        
        plot_buffer = io.BytesIO()
        plt.savefig(plot_buffer, format='png')
        plot_data["plot"] = base64.b64encode(plot_buffer.getvalue()).decode('utf-8')
        plt.close(fig)
    
    else:
        # Figure for user choice
        fig,ax=plt.subplots(ncols=3,figsize=(18,5))
        ax[0].imshow(img, origin="lower")
        ax[0].scatter(idx2, idx1, marker = 'x', color="red")
        ax[0].axes.xaxis.set_visible(False)
        ax[0].axes.yaxis.set_visible(False)
        ax[1].plot(new_spec_x, new_spec_y)
        ax[1].set_title('loc:' +str(idx2) +"," + str(idx1), fontsize = 20)
        ax[2].plot(new_spec_x,target_func)
        ax[2].set_title('Current target function', fontsize = 20)
        
        plot_buffer = io.BytesIO()
        plt.savefig(plot_buffer, format='png')
        plot_data["plot"] = base64.b64encode(plot_buffer.getvalue()).decode('utf-8')
        plt.close(fig)
    
    return plot_data
    
def initial_eval_loop_plot(initial_eval_loop_counter, train_indices, points_measured, last_points_measured, IV, vdc_vec, init_spec, eval_spec_y, m, img, wcount_good, target_func):
    #parameters_needed = loop_counter, trian_indices, points_measured, last_points_measured, IV, ved_vec, init_spec, eval_spec_y, m, pref, img, wcount_good, target_func
    idx_x = int(train_indices[initial_eval_loop_counter, 0])
    idx_y = int(train_indices[initial_eval_loop_counter, 1])
    next_loc = np.asarray([idx_x, idx_y])
    
    m1 = "i is {}, measurement done".format(initial_eval_loop_counter)
    
    mask = np.isin(points_measured, last_points_measured, invert = True)
    new_points_measured = points_measured[mask]
    last_points_measured = np.append(last_points_measured, new_points_measured)
    
    m2 = 'points measured {}'.format(points_measured)
    m3 = 'new_points_measured {}'.format(new_points_measured)
    
    new_iv = IV[last_points_measured,:]
    new_spec_x = vdc_vec
    new_spec_y = new_iv[initial_eval_loop_counter,:]
    
    new_spec_y = (new_spec_y - new_spec_y.min())/(new_spec_y.max() - new_spec_y.min())
    init_spec[initial_eval_loop_counter,] = new_spec_y
    eval_spec_y[idx_x, idx_y, :] = new_spec_y
    m4 = "\n\nSample #" + str(m + 1)
    
    plot_data = generate_plots_for_initial_eval(idx_x, idx_y, new_spec_x, new_spec_y, img, wcount_good, target_func)
    return {
        "plot_data": plot_data,
        "train_indices": train_indices,
        "points_measured": points_measured,
        "last_points_measured": last_points_measured,
        "IV": IV,
        "vdc_vec": vdc_vec,
        "init_spec": init_spec,
        "eval_spec_y": eval_spec_y,
        "m": m,
        "img": img,
        "wcount_good": wcount_good,
        "target_func": target_func,
        "new_spec_x": new_spec_x,
        "new_spec_y": new_spec_y,
    }

def initial_eval_vote_process(vote, newspec_pref, newspec_wt, wcount_good, target_func, new_spec_y, pref, m, initial_eval_loop_counter):
    
    newspec_wt_by_usr = newspec_wt/10
    if vote > 0:
        newspec_wt = 1
        if wcount_good > 0:
            if newspec_pref == 1:
                newspec_wt = newspec_wt_by_usr
            else:
                newspec_wt = 0.5
        wcount_good = wcount_good + vote
        target_func = (((1-newspec_wt)*target_func*(wcount_good-vote))+(newspec_wt*vote * new_spec_y))/(((wcount_good-vote)*(1-newspec_wt)) + (vote*newspec_wt))
    
    pref[initial_eval_loop_counter, 0] = vote
    m = m + 1
    initial_eval_loop_counter += 1
    
    return {
        "vote": vote,
        "newspec_pref": newspec_pref,
        "newspec_wt": newspec_wt,
        "pref": pref,
        "m": m,
        "initial_eval_loop_counter": initial_eval_loop_counter,
        "wcount_good": wcount_good,
        "target_func": target_func,
    }

def func_human_interacted_obj(idx_x, idx_y, new_spec_x, new_spec_y, wcount_good, target_func, vote):
    idx1 = int(idx_x)
    idx2 = int(idx_y)
    rf = 1
    #print(wcount_good)
    if (wcount_good == 0): #We dont find a good loop yet from all initial sampling and thus target is unknown
        ssim_spec = np.random.rand(1)*(1) # Unif[0, 1] A sufficiently large value as we want to avoid selecting bad loops,
        # When we have a target, we will recalculate again to get more accuract estimate
        R = vote*rf

    else:
        #Calculate dissimilarity (mse) between target and ith loop shape

        pred = new_spec_y
        target = target_func
        ssim_spec = ssim(target, pred, data_range=pred.max() - pred.min())
        #plt.plot(new_spec_x, new_spec_y)
        #plt.show()
        #dev2_spectral = (target_func-new_spec_y)**2
        #mse_spectral = torch.mean(dev2_spectral)
        #Calculate reward as per voting, this will minimize the risk of similar function values of good and bad loop shape with similar mse
        R = vote*rf

    #This is the basic setting of obj func-- we can incorporate more info as per domain knowledge to improve
    #Into maximization problem
    obj = R + ssim_spec #Maximize reward and ssim
    #print(mse_spectral)
    return obj

def initial_eval_finish(num_start, train_indices, eval_spec_y, train_Y, new_spec_x, wcount_good, target_func, pref, X_feas, X_feas_norm, train_X, train_X_norm, idx, m):
    #parameters_needed = num_start, train_indices, eval_spec_y, train_Y, new_spec_x, wcount_good, target_func, pref, X_feas, X_feas_norm, train_X, train_X_norm, idx, m
    for i in range(0, num_start):
        idx_x = int(train_indices[i, 0])
        idx_y = int(train_indices[i, 1])
        spec_y = eval_spec_y[idx_x, idx_y, :]
        
        train_Y[i, 0] = func_human_interacted_obj(idx_x, idx_y, new_spec_x, spec_y, wcount_good, target_func, pref[i, 0])
    
    var_params = [wcount_good, pref, target_func]
    test_X, test_X_norm, train_X, train_X_norm, train_Y, var_params, idx, m = X_feas, X_feas_norm, train_X, train_X_norm, train_Y, var_params, idx, m
    
    print("var_params: ", var_params)
    print("test_X: ", test_X)
    print("test_X_norm: ", test_X_norm)
    print("train_Y: ", train_Y)
    print("idx: ", idx)
    
    return {
        "train_Y": train_Y,
        "var_params": var_params,
        "test_X": test_X,
        "test_X_norm": test_X_norm,
        "train_X": train_X,
        "train_X_norm": train_X_norm,
        "idx": idx,
        "m": m,
    }