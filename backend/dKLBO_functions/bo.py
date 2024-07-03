import gpax
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import io
import base64
from scipy.stats import norm
import atomai as aoi
from atomai import utils
from skimage.metrics import structural_similarity as ssim


def plot_results(train_indices, train_Y, indices, y_pred_means, y_pred_vars, X_opt, X_opt_GP, img_space, i):
    pen = 10**0
    #Objective map
    fig,ax=plt.subplots(ncols=3,figsize=(18,5))
    a= ax[0].imshow(img_space, origin = "lower")
    ax[0].scatter(train_indices[:,1], train_indices[:,0], c=train_Y, cmap='jet', linewidth=0.2)
    ax[0].scatter(X_opt[0, 1], X_opt[0, 0], marker='x', c='r')
    ax[0].scatter(X_opt_GP[0, 1], X_opt_GP[0, 0], marker='o', c='r')
    ax[0].axes.xaxis.set_visible(False)
    ax[0].axes.yaxis.set_visible(False)

    a = ax[1].scatter(indices[:,1], indices[:,0], c=y_pred_means/pen, cmap='viridis', linewidth=0.2)
    ax[1].scatter(train_indices[:,1], train_indices[:,0], marker='o', c='g')
    ax[1].scatter(X_opt[0, 1], X_opt[0, 0], marker='x', c='r')
    ax[1].scatter(X_opt_GP[0, 1], X_opt_GP[0, 0], marker='o', c='r')
    divider = make_axes_locatable(ax[1])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(a, cax=cax, orientation='vertical')
    ax[1].set_title('Objective (GP mean) map', fontsize=10)
    ax[1].axes.xaxis.set_visible(False)
    ax[1].axes.yaxis.set_visible(False)
    #ax[1].colorbar(a)

    b = ax[2].scatter(indices[:,1], indices[:,0], c=y_pred_vars/(pen**2), cmap='viridis', linewidth=0.2)
    divider = make_axes_locatable(ax[2])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(b, cax=cax, orientation='vertical')
    ax[2].set_title('Objective (GP var) map', fontsize=10)
    ax[2].axes.xaxis.set_visible(False)
    ax[2].axes.yaxis.set_visible(False)
    #ax[2].colorbar(b)

    # plt.savefig('acquisition_results_step=' + str(i) +'.png', dpi = 300, bbox_inches = 'tight', pad_inches = 1.0)
    # plt.show()
    bo_plot_buffer = io.BytesIO()
    plt.savefig(bo_plot_buffer, format='png')
    bo_plot_data = base64.b64encode(bo_plot_buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    
    return bo_plot_data

def func_automated_obj(idx_x, idx_y, new_spec_x, new_spec_y, target_func, wcount_good):
    idx1 = int(idx_x)
    idx2 = int(idx_y)
    rf = 10
    #print(wcount_good)
    if (wcount_good == 0): #We dont find a good loop yet from all initial sampling and thus target is unknown
        ssim_spec = np.random.rand(1)*(1) # Unif[0, 1] A sufficiently large value as we want to avoid selecting bad loops,


    else:
        #Calculate ssim between target and ith loop shape
        pred = new_spec_y
        target = target_func
        ssim_spec = ssim(target, pred, data_range=pred.max() - pred.min())

    #This is the basic setting of obj func-- we can incorporate more info as per domain knowledge to improve
    #Into maximization problem
    obj = rf * ssim_spec  #Maximize reward and negative mse
    #print(obj)
    return obj
    
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

def return_new_measurement(full_dataset, points_measured):
    ampdat_masked = np.zeros_like(full_dataset)
    ampdat_masked[points_measured,:] = full_dataset[points_measured,:]
    return ampdat_masked, points_measured

def optimize_dKLgp(train_X, train_Y):
    data_dim = train_X.shape[-1]
    key1, key2 = gpax.utils.get_keys()
    dklgp_surro = gpax.viDKL(data_dim, z_dim=2, kernel='RBF')
    dklgp_surro.fit(key1, train_X, train_Y, num_steps=100, step_size=0.05)
    return dklgp_surro

def cal_posterior(gp_surro, test_X):
    y_pred_means = np.zeros((len(test_X), 1))
    y_pred_vars = np.zeros((len(test_X), 1))
    key1, key2 = gpax.utils.get_keys()
    mean, var = gp_surro.predict(key2, test_X)
    y_pred_means[:, 0] = mean
    y_pred_vars[:, 0] = var

    return y_pred_means, y_pred_vars

def estimate (train_indices, train_Y, indices, y_pred_means):
    #Best solution among the evaluated data
    loss = np.max(train_Y)
    ind = np.argmax(train_Y)
    X_opt = np.zeros((1,2))
    X_opt[0, 0] = train_indices[ind, 0]
    X_opt[0, 1] = train_indices[ind, 1]
    #print(loss, ind)

    # Best estimated solution from GP model considering the non-evaluated solution
    loss = np.max(y_pred_means)
    ind = np.argmax(y_pred_means)
    X_opt_GP = np.zeros((1,2))
    X_opt_GP[0, 0] = indices[ind, 0]
    X_opt_GP[0, 1] = indices[ind, 1]
    #print(loss, ind)

    return X_opt, X_opt_GP

def acqmanEI(y_means, y_vars, train_Y, ieval):
        ieval = np.array(ieval, dtype =np.int32)
        y_std = np.sqrt(y_vars)
        fmax = train_Y.max()
        best_value = fmax
        EI_val = np.zeros(len(y_vars))
        Z = np.zeros(len(y_vars))
        eta = 0.01

        for i in range(0, len(y_std)):
            if (y_std[i] <=0):
                EI_val[i] = 0
            else:
                Z[i] =  (y_means[i]-best_value-eta)/y_std[i]
                EI_val[i] = (y_means[i]-best_value-eta)*norm.cdf(Z[i]) + y_std[i]*norm.pdf(Z[i])

        EI_val[ieval] = -1
        acq_val = np.max(EI_val)
        acq_cand = [k for k, j in enumerate(EI_val) if j == acq_val]
        #print(acq_val)
        return acq_cand, acq_val, EI_val
    
def bo_setup(train_X_norm, train_Y):
    #parameters = train_X_norm, train_Y  
    
    print("train_X_norm = ", train_X_norm)
    print("train_Y = ", train_Y) 
     
    switch_obj_index = 0
    gp_surro = optimize_dKLgp(train_X_norm, train_Y[:,0])
    
    print("switch_obj_index = ", switch_obj_index)
    print("gp_surro = ", gp_surro)
    return {
        "switch_obj_index": switch_obj_index,
        "gp_surro": gp_surro,
    }

def bo_loop_first_step(bo_loop_counter, gp_surro, test_X_norm, train_indices, train_Y, indices, img, idx, X_eval, X_GP):
    #parameters = bo_loop_counter, gp_surro, test_X_norm, train_indices, train_Y, indices, img, idx
    print("idx = ", idx)
    print("train_indices = ", train_indices)
    print("train_Y = ", train_Y)
    bo_loop_counter = bo_loop_counter + 1
    i = bo_loop_counter
    y_pred_means, y_pred_vars = cal_posterior(gp_surro, test_X_norm)
    fig = None
    if ((i == 1) or ((i % 10) == 0)):
        X_eval, X_GP = estimate(train_indices, train_Y, indices, y_pred_means)
        fig = plot_results(train_indices, train_Y, indices, y_pred_means, y_pred_vars, X_eval, X_GP, img, i)
    acq_cand, acq_val, EI_val = acqmanEI(y_pred_means, y_pred_vars, train_Y, idx)
    val = acq_val
    ind = np.random.choice(acq_cand)
    idx = np.hstack((idx, ind))
    
    print("y_pred_means = ", y_pred_means)
    print("y_pred_vars = ", y_pred_vars)
    print("X_eval = ", X_eval)
    print("X_GP = ", X_GP)
    print("acq_cand = ", acq_cand)
    print("acq_val = ", acq_val)
    print("EI_val = ", EI_val)
    print("val = ", val)
    print("ind = ", ind)
    print("idx = ", idx)
    print("bo_loop_counter = ", bo_loop_counter)
    
    return  {
        "y_pred_means": y_pred_means,
        "y_pred_vars": y_pred_vars,
        "X_eval": X_eval,
        "X_GP": X_GP,
        "fig": fig,
        "acq_cand": acq_cand,
        "acq_val": acq_val,
        "EI_val": EI_val,
        "val": val,
        "ind": ind,
        "idx": idx,
        "bo_loop_counter": bo_loop_counter
    }
    
def bo_loop_second_step(bo_loop_counter, val, break_bo, test_X, test_X_norm, indices, ind, idx, targets, vdc_vec, eval_spec_y, img):
    #parameters = bo_loop_counter, val, break_bo
    i = bo_loop_counter
    if (i == 1):
        val_ini = val
    if ((val) < 0):  # Stop for negligible expected improvement
        print("Model converged due to sufficient learning over search space ")
        break_bo = 1
    else:
        nextX = np.zeros((1, test_X.shape[1]))
        nextX_norm = np.zeros((1, test_X_norm.shape[1]))
        next_indices = np.zeros((1,2))
        nextX[0,:] = test_X[ind, :]
        nextX_norm [0, :] = test_X_norm[ind, :]
        next_indices[0, :] = indices[ind, :]
        idx_x = int(next_indices[0, 0])
        idx_y = int(next_indices[0, 1])
        
        next_loc = np.asarray([idx_x, idx_y])
        new_points_measured = idx
        
        print("new_points_measured = ", new_points_measured)
        print("targets = ", targets)
        IV, points_measured = return_new_measurement(targets, new_points_measured)
        new_iv = IV[points_measured,:]
        print("IV = ", IV)
        print("points_measured = ", points_measured)
        print("new_iv = ", new_iv)
        
        new_spec_x = vdc_vec
        new_spec_y = new_iv[-1]
        print("new_spec_x = ", new_spec_x)
        print("new_spec_y = ", new_spec_y)
        
        new_spec_y = (new_spec_y - new_spec_y.min())/(new_spec_y.max() - new_spec_y.min())
        print("new_spec_y = ", new_spec_y)
        
        eval_spec_y[idx_x, idx_y, :] = new_spec_y
    
    print("nextX = ", nextX)
    print("nextX_norm = ", nextX_norm)
    print("next_indices = ", next_indices)
    print("idx_x = ", idx_x)
    print("idx_y = ", idx_y)
    print("next_loc = ", next_loc)
    print("new_points_measured = ", new_points_measured)
    print("IV = ", IV)
    print("points_measured = ", points_measured)
    print("new_spec_x = ", new_spec_x)
    print("new_spec_y = ", new_spec_y)
    print("eval_spec_y = ", eval_spec_y)
    print("break_bo = ", break_bo)
    
    return {
        "nextX": nextX,
        "nextX_norm": nextX_norm,
        "next_indices": next_indices,
        "idx_x": idx_x,
        "idx_y": idx_y,
        "next_loc": next_loc,
        "new_points_measured": new_points_measured,
        "IV": IV,
        "points_measured": points_measured,
        "new_spec_x": new_spec_x,
        "new_spec_y": new_spec_y,
        "eval_spec_y": eval_spec_y,
        "break_bo": break_bo
    }

def bo_loop_third_step(next_indices, train_indices, eval_spec_y, img, nextX_norm, train_X_norm):
    
    nextind = next_indices
    train_indices = np.vstack((train_indices, nextind))
    
    window_size = 4
    features, targets, indices = aoi.utils.extract_patches_and_spectra(eval_spec_y, img, coordinates=train_indices, window_size=window_size, avg_pool=1)
    norm_ = lambda x: (x - x.min()) / x.ptp()
    features, targets = norm_(features), norm_(targets)
    
    features = features.reshape(-1, window_size*window_size)
    
    #Ask Arpan
    train_X_norm = np.vstack((train_X_norm, nextX_norm))
    train_X = features
    train_X_norm = features
    
    idx = np.zeros((len(features), 1))
    num_cols = img.shape[-1]
    train_Y = np.empty((len(features), 1))
    
    p = np.zeros((1, 1))
    idx_x = int(train_indices[-1, 0])
    idx_y = int(train_indices[-1, 1])
    
    print("train_X", train_X)
    print("train_X_norm", train_X_norm)
    print("train_indices", train_indices)
    print("train_Y", train_Y)
    print("num_cols", num_cols)
    print("idx", idx)
    print("features", features)
    print("targets", targets)
    print("idx_x", idx_x)
    print("idx_y", idx_y)
    print("indices", indices)
    
    return {
        "train_X": train_X,
        "train_X_norm": train_X_norm,
        "train_indices": train_indices,
        "train_Y": train_Y,
        "num_cols": num_cols,
        "idx": idx,
        "features": features,
        "targets": targets,
        "idx_x": idx_x,
        "idx_y": idx_y,
        "indices": indices,
        "p": p
    }

def bo_loop_fourth_step_satisfied(new_spec_x, new_spec_y, idx_y, idx_x, features, indices, idx, num_cols, targets, train_Y, m, var_params):

    wcount_good, pref, target_func = var_params[0], var_params[1], var_params[2]
    plt.plot(new_spec_x, new_spec_y)
    plt.title('loc:' +str(idx_y) +"," + str(idx_x), fontsize = 20)
    # plt.show()
    print("Satisfaction plotted")
    for i in range(len(features)):
        idx_x = int(indices[i, 0])
        idx_y = int(indices[i, 1])
        idx[i,:] = [idx_x*num_cols + idx_y]
        spec_y = targets[i,:]
        #print(idx_x, idx_y, spec_y)
        print ("idx_x = ", idx_x)
        print ("idx_y = ", idx_y)
        print ("spec_y = ", spec_y)
        print("idx = ", idx)
        print("train_Y = ", train_Y)
        train_Y[i, 0] = func_automated_obj(idx_x, idx_y, new_spec_x, spec_y, target_func, wcount_good)
        print("train_Y = ", train_Y)
    
    m = m + 1
    var_params = [wcount_good, pref, target_func]
    return {
        "train_Y": train_Y,
        "m": m,
        "var_params": var_params
    }

def bo_loop_fourth_step_unsatisfied_plot(idx_x, idx_y, new_spec_x, new_spec_y, img, var_params):
    #parameters_needed = idx_x, idx_y, new_spec_x, new_spec_y, img, wcount_good, target_func
    wcount_good, pref, target_func = var_params[0], var_params[1], var_params[2]
    
    idx1 = int(idx_x)
    idx2 = int(idx_y)

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
        plot = base64.b64encode(plot_buffer.getvalue()).decode('utf-8')
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
        plot = base64.b64encode(plot_buffer.getvalue()).decode('utf-8')
        plt.close(fig)
    
    return {
        "plot": plot
    }

def bo_loop_fourth_step_unsatisfied_vote_process(vote, newspec_pref, newspec_wt, var_params, new_spec_y):
    
    wcount_good, pref, target_func = var_params[0], var_params[1], var_params[2]
    
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
    
    var_params = [wcount_good, pref, target_func]
    return {
        "vote": vote,
        "newspec_pref": newspec_pref,
        "newspec_wt": newspec_wt,
        "var_params": var_params
    }

def bo_loop_fourth_step_unsatisfied(p, vote, var_params, features, indices, idx, num_cols, targets, train_Y, new_spec_x, m):
    
    wcount_good, pref, target_func = var_params[0], var_params[1], var_params[2]
    
    p[0,0] = vote
    pref = np.vstack((pref, p))
    for i in range(len(features)):
        idx_x = int(indices[i, 0])
        idx_y = int(indices[i, 1])
        idx[i,:] = [idx_x*num_cols + idx_y]
        spec_y = targets[i,:]
        #print(idx_x, idx_y, spec_y)
        train_Y[i, 0] = func_human_interacted_obj(idx_x, idx_y, new_spec_x, spec_y, wcount_good, target_func, pref[i, 0])
    
    m = m + 1
    var_params = [wcount_good, pref, target_func]
    
    return {
        "train_Y": train_Y,
        "m": m,
        "var_params": var_params
    }

def bo_loop_fifth_step(train_X_norm, train_Y):
    gp_surro = optimize_dKLgp(train_X_norm, train_Y[:, 0])
    return {
        "gp_surro": gp_surro
    }
    
    

def bo_loop_automated(bo_loop_counter, num_bo, test_X_norm, indices, img, test_X, targets, vdc_vec, eval_spec_y, gp_surro, train_indices, train_Y, idx, train_X, train_X_norm, var_params, switch_obj_index, m, X_eval, X_GP):
    figures = []
    location_plots = []
    if (num_bo - bo_loop_counter) <= 5:
        num_iter = num_bo
    else:
        num_iter = bo_loop_counter + 5
    for i in range(bo_loop_counter + 1, num_iter + 1):
        print("Step# ", i)
        y_pred_means, y_pred_vars = cal_posterior(gp_surro, test_X_norm)

        if ((i == 1) or ((i % 10) == 0)):
            X_eval, X_GP = estimate(train_indices, train_Y, indices, y_pred_means)
            fig = plot_results(train_indices, train_Y, indices, y_pred_means, y_pred_vars, X_eval, X_GP, img, i)
            figures.append(fig)

        acq_cand, acq_val, EI_val = acqmanEI(y_pred_means, y_pred_vars, train_Y, idx)
        val = acq_val
        ind = np.random.choice(acq_cand)
        idx = np.hstack((idx, ind))

        if (i == 1):
            val_ini = val
        if ((val) < 0):  # Stop for negligible expected improvement
            print("Model converged due to sufficient learning over search space ")
            break
        else:
            nextX = np.zeros((1, test_X.shape[1]))
            nextX_norm = np.zeros((1, test_X_norm.shape[1]))
            next_indices = np.zeros((1,2))
            nextX[0,:] = test_X[ind, :]
            nextX_norm [0, :] = test_X_norm[ind, :]
            next_indices[0, :] = indices[ind, :]
            idx_x = int(next_indices[0, 0])
            idx_y = int(next_indices[0, 1])

            next_loc = np.asarray([idx_x, idx_y])
            new_points_measured = idx

            #polarization loop area
            IV, points_measured = return_new_measurement(targets, new_points_measured)

            new_iv = IV[points_measured,:]

            #new_spec_x = torch.from_numpy(vdc_vec)
            #new_spec_y = torch.from_numpy(new_iv)[-1]

            new_spec_x = vdc_vec
            new_spec_y = new_iv[-1]


            new_spec_y = (new_spec_y - new_spec_y.min())/(new_spec_y.max() - new_spec_y.min())

            #clear_output(wait=True) Comment out as I need to check the run in colab

            eval_spec_y[idx_x, idx_y, :] = new_spec_y
            # Evaluate true function for new data, augment data
            train_X, train_X_norm, _, train_indices, train_Y, var_params, switch_obj_index, m, location_plot = augment_newdata_KL_satisfied(nextX, nextX_norm, next_indices, train_X, train_X_norm, train_indices, train_Y, new_spec_x, new_spec_y, eval_spec_y, img, var_params, switch_obj_index, m, bo_loop_counter = i)

            location_plots.append(location_plot)
            gp_surro = optimize_dKLgp(train_X_norm, train_Y[:, 0])
    
    bo_loop_counter = bo_loop_counter + (num_iter - bo_loop_counter)
    return {
        "bo_loop_counter": bo_loop_counter,
        "figures": figures,
        "gp_surro": gp_surro,
        "test_X_norm": test_X_norm,
        "train_indices": train_indices,
        "train_Y": train_Y,
        "indices": indices,
        "X_eval": X_eval,
        "X_GP": X_GP,
        "img": img,
        "var_params": var_params,
        "location_plots": location_plots,
    }

def bo_finish(gp_surro, test_X_norm, train_indices, train_Y, indices, X_eval, X_GP, img, bo_loop_counter, var_params):
    
    i = bo_loop_counter
    gp_opt = gp_surro
    y_pred_means, y_pred_vars = cal_posterior(gp_opt, test_X_norm)
    X_opt, X_opt_GP = estimate(train_indices, train_Y, indices, y_pred_means)
    final_plot = plot_results(train_indices, train_Y, indices, y_pred_means, y_pred_vars, X_eval, X_GP, img, i)
    explored_data = [train_indices, train_indices, train_Y]
    final_GP_estim = [y_pred_means, y_pred_vars]
    user_votes = var_params[1]
    optim_results = [X_opt, X_opt_GP, user_votes, explored_data]
    
    optim_results = {
        'X_opt': X_opt,
        'X_opt_GP': X_opt_GP,
        'user_votes': user_votes,
        'explored_data_train_indices': train_indices,
        'explored_data_train_Y': train_Y,
    }
    
    np.save('./optim_results.npy', optim_results)
    
    return {
        "gp_opt": gp_opt,
        "y_pred_means": y_pred_means,
        "y_pred_vars": y_pred_vars,
        "X_opt": X_opt,
        "X_opt_GP": X_opt_GP,
        "final_plot": final_plot,
        "explored_data": explored_data,
        "final_GP_estim": final_GP_estim,
        "user_votes": user_votes,
        "optim_results": optim_results
    }

def augment_newdata_KL_satisfied(acq_X, acq_X_norm, acq_indices, train_X, train_X_norm, train_indices, train_Y,
                           new_spec_x, new_spec_y, eval_spec, img_space, var_params, u, m, bo_loop_counter):
        
    #check_with_arpan
    eval_spec_y = eval_spec
    img = img_space
    nextX, nextX_norm = acq_X, acq_X_norm
    
    wcount_good, pref, target_func = var_params[0], var_params[1], var_params[2]

    #coordinates = aoi.utils.get_coord_grid(img, step=1, return_dict=False)
    nextind = acq_indices
    train_indices = np.vstack((train_indices, nextind))
    #train_indices = torch.from_numpy(train_indices)

    window_size = 4
    features, targets, indices = aoi.utils.extract_patches_and_spectra(eval_spec_y, img, coordinates=train_indices, window_size=window_size, avg_pool=1)
    norm_ = lambda x: (x - x.min()) / x.ptp()
    features, targets = norm_(features), norm_(targets)

    features = features.reshape(-1, window_size*window_size)
    #print(train_indices.shape, features.shape, targets.shape)


    #nextX = acq_X
    #nextX_norm = acq_X_norm

    train_X_norm = np.vstack((train_X_norm, nextX_norm))
    #train_X = np.vstack((train_X, nextX))
    train_X = features
    train_X_norm = features
    print(train_X.shape, train_X_norm.shape)

    idx = np.zeros((len(features), 1))
    num_cols = img.shape[-1]
    train_Y = np.empty((len(features), 1))

    p = np.zeros((1, 1))
    #x = torch.empty((1,2))
    idx_x = int(train_indices[-1, 0])
    idx_y = int(train_indices[-1, 1])

    # plt.plot(new_spec_x, new_spec_y)
    # plt.title('loc:' +str(idx_y) +"," + str(idx_x), fontsize = 20)
    # plt.show()

    # location_plot_buffer = io.BytesIO()
    # plt.savefig(location_plot_buffer, format='png')
    # location_plot = base64.b64encode(location_plot_buffer.getvalue()).decode('utf-8')

    loc_fig, loc_ax = plt.subplots(ncols=2, figsize=(12,5))
    loc_ax[0].plot(new_spec_x, new_spec_y)
    loc_ax[0].set_title(f'loc: {idx_y},{idx_x}', fontsize=20)
    loc_ax[1].plot(new_spec_x, target_func)
    loc_ax[1].set_title('Target function', fontsize = 20)
    
    loc_fig.suptitle(f'BO Iteration #{bo_loop_counter}', fontsize=20)
    
    location_plot_buffer = io.BytesIO()
    plt.savefig(location_plot_buffer, format='png')
    location_plot = base64.b64encode(location_plot_buffer.getvalue()).decode('utf-8')
    
    plt.close(loc_fig)
    
    for i in range(len(features)):
        idx_x = int(indices[i, 0])
        idx_y = int(indices[i, 1])
        idx[i,:] = [idx_x*num_cols + idx_y]
        spec_y = targets[i,:]
        #print(idx_x, idx_y, spec_y)
        train_Y[i, 0] = func_automated_obj(idx_x, idx_y, new_spec_x, spec_y, target_func, wcount_good)

    var_params = [wcount_good, pref, target_func]
    m = m + 1
    return train_X, train_X_norm, indices, train_indices, train_Y, var_params, u, m, location_plot