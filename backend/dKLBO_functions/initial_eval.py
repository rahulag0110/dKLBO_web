import numpy as np
import matplotlib.pyplot as plt
import base64
import io

def return_new_measurement(full_dataset, points_measured):
    ampdat_masked = np.zeros_like(full_dataset)
    ampdat_masked[points_measured,:] = full_dataset[points_measured,:]
    return ampdat_masked, points_measured

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
    

def initial_eval(amp_masked, idx, vdc_vec, num_start, img, spec_length):
    #parameters_needed = amp_masked, idx, vdc_vec, num_start, img, spec_length
    # set parameters
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
    
    return {
        "IV": IV,
        "points_measured": points_measured,
        "last_points_measured": last_points_measured,
        # "vdc": vdc,
        # "train_Y": train_Y,
        "pref": pref,
        "init_spec": init_spec,
        "eval_spec_y": eval_spec_y,
        # "x": x,
        "wcount_good": wcount_good,
        "target_func": target_func,
        # "new_points_measured": new_points_measured
        }

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
        "new_spec_y": new_spec_y,
    }

def initial_eval_vote_process(vote, newspec_pref, newspec_wt, wcount_good, target_func, new_spec_y, pref, m, initial_eval_loop_counter):
    
    if vote > 0:
        newspec_wt = 1
        if wcount_good > 0:
            if newspec_pref == 1:
                newspec_wt = newspec_wt
            else:
                newspec_wt = 0.5
        wcount_good = wcount_good + vote
        target_func = (((1-newspec_wt)*target_func*(wcount_good-vote))+(newspec_wt*vote * new_spec_y))/(((wcount_good-vote)*(1-newspec_wt)) + (vote*newspec_wt))
    
    pref[initial_eval_loop_counter, 0] = vote
    m = m + 1
    initial_eval_loop_counter += 1
    
    return {
        "pref": pref,
        "m": m,
        "initial_eval_loop_counter": initial_eval_loop_counter,
        "wcount_good": wcount_good,
        "target_func": target_func,
    }