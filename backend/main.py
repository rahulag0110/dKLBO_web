from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pickle

from dKLBO_functions.preprocess import preprocess
from dKLBO_functions.initial_eval import initial_eval_loop_plot, initial_eval_vote_process, initial_eval_finish
from dKLBO_functions.bo import bo_setup, bo_loop_first_step, bo_loop_second_step, bo_loop_third_step, bo_loop_fourth_step_satisfied, bo_loop_fourth_step_unsatisfied_plot, bo_loop_fourth_step_unsatisfied_vote_process, bo_loop_fourth_step_unsatisfied, bo_loop_fifth_step, bo_loop_automated, bo_finish

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store the return values of the functions
class NumStart(BaseModel):
    num_start: int

class NumBO(BaseModel):
    num_bo: int

class Rating(BaseModel):
    vote: int
    newspec_pref: int
    newspec_wt: int

parameters_state = {
    "spec_length": None,
    "idx": None,
    "vdc_vec": None,
    "num_start": None,
    "img": None,
    "amp_masked": None,
    "train_indices": None,
    "m": None,
    "points_measured": None,
    "last_points_measured": None,
    "IV": None,
    "init_spec": None,
    "eval_spec_y": None,
    "img" : None,
    "X_feas": None,
    "X_feas_norm": None,
    "train_X": None,
    "train_X_norm": None,
    "new_spec_x": None,
    "new_spec_y": None,
    "train_Y": None,
    "pref": None,
    "wcount_good": None,
    "target_func": None,
    "initial_eval_loop_counter": None,
    "plot_history": [],
    "num_bo": None,
    "gp_surro": None,
    "switch_obj_index": None,
    "bo_plots": [],
    "indices": None,
    "bo_loop_counter": None,
    "var_params": None,
    "test_X": None,
    "test_X_norm": None,
    "y_pred_means": None,
    "y_pred_vars": None,
    "X_eval": None,
    "X_GP": None,
    "acq_cand": None,
    "acq_val": None,
    "EI_val": None,
    "val": None,
    "ind": None,
    "break_bo": None,
    "targets": None,
    "nextX": None,
    "nextX_norm": None,
    "next_indices": None,
    "idx_x": None,
    "idx_y": None,
    "next_loc": None,
    "new_points_measured": None,
    "optim_results": None
}

@app.get("/")
async def read_root():
    return {"Server Running"}

@app.post("/set_num_start/")
async def set_num_start(num_start: NumStart):
    global parameters_state
    parameters_state["num_start"] = num_start.num_start
    return {"status": "num_start set successfully"}

@app.post("/upload/")
async def process_file(file: UploadFile = File(...)):
    global parameters_state
    # Temporarily store file on disk
    with open("temp_large_file.p", "wb") as temp_file:
        # Read and write the file in chunks
        while content := await file.read(1024*1024):  # read in 1MB chunks
            temp_file.write(content)

    # Open the temporary file in read mode and process
    with open("temp_large_file.p", "rb") as f:
        try:
            uploaded_file = pickle.load(f)
        except Exception as e:
            return {"Read error": str(e)}

    import os
    os.remove("temp_large_file.p")
    
    print("File uploaded successfully")  
    num_start = parameters_state["num_start"]  
    preprocess_return = preprocess(uploaded_file, num_start)
    parameters_state["spec_length"] = preprocess_return["spec_length"]
    parameters_state["idx"] = preprocess_return["idx"]
    parameters_state["vdc_vec"] = preprocess_return["vdc_vec"]
    parameters_state["num_start"] = preprocess_return["num_start"]
    parameters_state["img"] = preprocess_return["img"]
    parameters_state["X_feas"] = preprocess_return["X_feas"]
    parameters_state["X_feas_norm"] = preprocess_return["X_feas_norm"]
    parameters_state["train_X"] = preprocess_return["train_X"]
    parameters_state["train_X_norm"] = preprocess_return["train_X_norm"]
    parameters_state["amp_masked"] = preprocess_return["amp_masked"]
    parameters_state["train_indices"] = preprocess_return["train_indices"]
    parameters_state["m"] = preprocess_return["m"]
    parameters_state["points_measured"] = preprocess_return["points_measured"]
    parameters_state["last_points_measured"] = preprocess_return["last_points_measured"]
    parameters_state["IV"] = preprocess_return["IV"]
    parameters_state["init_spec"] = preprocess_return["init_spec"]
    parameters_state["eval_spec_y"] = preprocess_return["eval_spec_y"]
    parameters_state["train_Y"] = preprocess_return["train_Y"]
    parameters_state["pref"] = preprocess_return["pref"]
    parameters_state["wcount_good"] = preprocess_return["wcount_good"]
    parameters_state["target_func"] = preprocess_return["target_func"]
    parameters_state["initial_eval_loop_counter"] = preprocess_return["initial_eval_loop_counter"]
    parameters_state["indices"] = preprocess_return["indices"]
    parameters_state["targets"] = preprocess_return["targets"]
    
    # print(preprocess_return)
    return {"status": "file upload success", "num_start": parameters_state["num_start"], "initial_eval_loop_counter": parameters_state["initial_eval_loop_counter"]}
    
@app.post("/initial_eval_loop_plot/")
async def initial_eval_loop_endpoint():
    global parameters_state
    
    initial_eval_loop_counter = parameters_state["initial_eval_loop_counter"]
    train_indices = parameters_state["train_indices"]
    points_measured = parameters_state["points_measured"]
    last_points_measured = parameters_state["last_points_measured"]
    IV = parameters_state["IV"]
    vdc_vec = parameters_state["vdc_vec"]
    init_spec = parameters_state["init_spec"]
    eval_spec_y = parameters_state["eval_spec_y"]
    m = parameters_state["m"]
    img = parameters_state["img"]
    wcount_good = parameters_state["wcount_good"]
    target_func = parameters_state["target_func"]

    
    initial_eval_loop_return = initial_eval_loop_plot(initial_eval_loop_counter, train_indices, points_measured, last_points_measured, IV, vdc_vec, init_spec, eval_spec_y, m, img, wcount_good, target_func)
    parameters_state["train_indices"] = initial_eval_loop_return["train_indices"]
    parameters_state["points_measured"] = initial_eval_loop_return["points_measured"]
    parameters_state["last_points_measured"] = initial_eval_loop_return["last_points_measured"]
    parameters_state["IV"] = initial_eval_loop_return["IV"]
    parameters_state["vdc_vec"] = initial_eval_loop_return["vdc_vec"]
    parameters_state["init_spec"] = initial_eval_loop_return["init_spec"]
    parameters_state["eval_spec_y"] = initial_eval_loop_return["eval_spec_y"]
    parameters_state["m"] = initial_eval_loop_return["m"]
    parameters_state["img"] = initial_eval_loop_return["img"]
    parameters_state["wcount_good"] = initial_eval_loop_return["wcount_good"]
    parameters_state["target_func"] = initial_eval_loop_return["target_func"]
    parameters_state["new_spec_x"] = initial_eval_loop_return["new_spec_x"]
    parameters_state["new_spec_y"] = initial_eval_loop_return["new_spec_y"]
    plot_data = initial_eval_loop_return["plot_data"]
    plot_history_item = {"plot_data": plot_data, "rating": None}
    parameters_state["plot_history"].append(plot_history_item)
    
    
    return {"status": "initial_eval_loop success", "plot_data": plot_data, "current_wcount_good": parameters_state["wcount_good"], "plot_history": parameters_state["plot_history"], "num_start": parameters_state["num_start"], "initial_eval_loop_counter": parameters_state["initial_eval_loop_counter"]}

@app.post("/initial_eval_vote_process/")
async def initial_eval_vote_process_endpoint(rating: Rating):
    global parameters_state

    vote = rating.vote
    newspec_pref = rating.newspec_pref
    newspec_wt = rating.newspec_wt
    wcount_good = parameters_state["wcount_good"]
    target_func = parameters_state["target_func"]
    new_spec_y = parameters_state["new_spec_y"]
    pref = parameters_state["pref"]
    m = parameters_state["m"]
    initial_eval_loop_counter = parameters_state["initial_eval_loop_counter"]
    
    initial_eval_vote_process_return = initial_eval_vote_process(vote, newspec_pref, newspec_wt, wcount_good, target_func, new_spec_y, pref, m, initial_eval_loop_counter)
    
    parameters_state["pref"] = initial_eval_vote_process_return["pref"]
    parameters_state["m"] = initial_eval_vote_process_return["m"]
    parameters_state["initial_eval_loop_counter"] = initial_eval_vote_process_return["initial_eval_loop_counter"]
    parameters_state["wcount_good"] = initial_eval_vote_process_return["wcount_good"]
    parameters_state["target_func"] = initial_eval_vote_process_return["target_func"]
    
    rating = {"vote": initial_eval_vote_process_return["vote"], "newspec_pref": initial_eval_vote_process_return["newspec_pref"], "newspec_wt": initial_eval_vote_process_return["newspec_wt"]}
    parameters_state["plot_history"][-1]["rating"] = rating
    
    return {"status": "initial_eval_vote_process success", "initial_eval_loop_counter": parameters_state["initial_eval_loop_counter"], "plot_history": parameters_state["plot_history"], "num_start": parameters_state["num_start"]}

@app.post("/initial_eval_finish/")
async def initial_eval_finish_endpoint():
    global parameters_state
    
    num_start = parameters_state["num_start"]
    train_indices = parameters_state["train_indices"]
    eval_spec_y = parameters_state["eval_spec_y"]
    train_Y = parameters_state["train_Y"]
    new_spec_x = parameters_state["new_spec_x"]
    wcount_good = parameters_state["wcount_good"]
    target_func = parameters_state["target_func"]
    pref = parameters_state["pref"]
    X_feas = parameters_state["X_feas"]
    X_feas_norm = parameters_state["X_feas_norm"]
    train_X = parameters_state["train_X"]
    train_X_norm = parameters_state["train_X_norm"]
    idx = parameters_state["idx"]
    m = parameters_state["m"]
    
    initial_eval_finish_return = initial_eval_finish(num_start, train_indices, eval_spec_y, train_Y, new_spec_x, wcount_good, target_func, pref, X_feas, X_feas_norm, train_X, train_X_norm, idx, m)

    parameters_state["train_Y"] = initial_eval_finish_return["train_Y"]
    parameters_state["var_params"] = initial_eval_finish_return["var_params"]
    parameters_state["test_X"] = initial_eval_finish_return["test_X"]
    parameters_state["test_X_norm"] = initial_eval_finish_return["test_X_norm"]
    parameters_state["train_X"] = initial_eval_finish_return["train_X"]
    parameters_state["train_X_norm"] = initial_eval_finish_return["train_X_norm"]
    parameters_state["idx"] = initial_eval_finish_return["idx"]
    parameters_state["m"] = initial_eval_finish_return["m"]
    
    train_Y_str = initial_eval_finish_return["train_Y"].tolist()
    
    return {"status": "initial_eval_finish success", "train_Y": train_Y_str}

@app.post("/bo_setup/")
async def bo_setup_endpoint():
    global parameters_state
    
    train_X_norm = parameters_state["train_X_norm"]
    train_Y = parameters_state["train_Y"]
    
    bo_setup_return = bo_setup(train_X_norm, train_Y)
    
    parameters_state["gp_surro"] = bo_setup_return["gp_surro"]
    parameters_state["switch_obj_index"] = bo_setup_return["switch_obj_index"]
    parameters_state["bo_loop_counter"] = 0
    
    
    return {"status": "bo_setup success", "num_bo": parameters_state["num_bo"], "bo_loop_counter": parameters_state["bo_loop_counter"]}

@app.post("/set_num_bo/")
async def set_num_bo(num_bo: NumBO):
    global parameters_state
    parameters_state["num_bo"] = num_bo.num_bo
    return {"status": "num_bo set successfully"}

@app.post("/bo_loop_first_step/")
async def bo_loop_first_step_endpoint():
    global parameters_state
    
    bo_loop_counter = parameters_state["bo_loop_counter"]
    gp_surro = parameters_state["gp_surro"]
    test_X_norm = parameters_state["test_X_norm"]
    train_indices = parameters_state["train_indices"]
    train_Y = parameters_state["train_Y"]
    indices = parameters_state["indices"]
    img = parameters_state["img"]
    idx = parameters_state["idx"]
    X_eval = parameters_state["X_eval"]
    X_GP = parameters_state["X_GP"]
    
    bo_loop_first_step_return = bo_loop_first_step(bo_loop_counter, gp_surro, test_X_norm, train_indices, train_Y, indices, img, idx, X_eval, X_GP)
    

    parameters_state["y_pred_means"] = bo_loop_first_step_return["y_pred_means"]
    parameters_state["y_pred_vars"] = bo_loop_first_step_return["y_pred_vars"]
    parameters_state["X_eval"] = bo_loop_first_step_return["X_eval"]
    parameters_state["X_GP"] = bo_loop_first_step_return["X_GP"]
    parameters_state["acq_cand"] = bo_loop_first_step_return["acq_cand"]
    parameters_state["acq_val"] = bo_loop_first_step_return["acq_val"]
    parameters_state["EI_val"] = bo_loop_first_step_return["EI_val"]
    parameters_state["val"] = bo_loop_first_step_return["val"]
    parameters_state["ind"] = bo_loop_first_step_return["ind"]
    parameters_state["idx"] = bo_loop_first_step_return["idx"]
    parameters_state["bo_plots"].append(bo_loop_first_step_return["fig"])
    parameters_state["bo_loop_counter"] = bo_loop_first_step_return["bo_loop_counter"]
    
    
    return {"status": "bo_loop_first_step success", "bo_loop_counter": parameters_state["bo_loop_counter"], "bo_plots": parameters_state["bo_plots"]}

@app.post("/bo_loop_second_step/")
async def bo_loop_second_step_endpoint():
    global parameters_state
    
    bo_loop_counter = parameters_state["bo_loop_counter"]
    val = parameters_state["val"]
    break_bo = parameters_state["break_bo"]
    test_X = parameters_state["test_X"]
    test_X_norm = parameters_state["test_X_norm"]
    indices = parameters_state["indices"]
    ind = parameters_state["ind"]
    idx = parameters_state["idx"]
    targets = parameters_state["targets"]
    vdc_vec = parameters_state["vdc_vec"]
    eval_spec_y = parameters_state["eval_spec_y"]
    img = parameters_state["img"]
    
    bo_loop_second_step_return = bo_loop_second_step(bo_loop_counter, val, break_bo, test_X, test_X_norm, indices, ind, idx, targets, vdc_vec, eval_spec_y, img)
    
    parameters_state["nextX"] = bo_loop_second_step_return["nextX"]
    parameters_state["nextX_norm"] = bo_loop_second_step_return["nextX_norm"]
    parameters_state["next_indices"] = bo_loop_second_step_return["next_indices"]
    parameters_state["idx_x"] = bo_loop_second_step_return["idx_x"]
    parameters_state["idx_y"] = bo_loop_second_step_return["idx_y"]
    parameters_state["next_loc"] = bo_loop_second_step_return["next_loc"]
    parameters_state["new_points_measured"] = bo_loop_second_step_return["new_points_measured"]
    parameters_state["IV"] = bo_loop_second_step_return["IV"]
    parameters_state["points_measured"] = bo_loop_second_step_return["points_measured"]
    parameters_state["new_spec_x"] = bo_loop_second_step_return["new_spec_x"]
    parameters_state["new_spec_y"] = bo_loop_second_step_return["new_spec_y"]
    parameters_state["eval_spec_y"] = bo_loop_second_step_return["eval_spec_y"]
    parameters_state["break_bo"] = bo_loop_second_step_return["break_bo"]
    
    print("bo_loop_second_step success")
    print("BO LOOP COUNTER: ", parameters_state["bo_loop_counter"])
    print("BREAK BO: ", parameters_state["break_bo"])
    return {"status": "bo_loop_second_step success", "break_bo": parameters_state["break_bo"], "bo_loop_counter": parameters_state["bo_loop_counter"]}

aug_func_state = {
    "train_X": None,
    "train_X_norm": None,
    "train_indices": None,
    "train_Y": None,
    "num_cols": None,
    "idx": None,
    "features": None,
    "targets": None,
    "idx_x": None,
    "idx_y": None,
    "indices": None,
    "p": None,
    "vote": None
    }

@app.post("/bo_loop_third_step/")
async def bo_loop_third_step_endpoint():
    global parameters_state
    global aug_func_state
    
    next_indices = parameters_state["next_indices"]
    train_indices = parameters_state["train_indices"]
    eval_spec_y = parameters_state["eval_spec_y"]
    img = parameters_state["img"]
    nextX_norm = parameters_state["nextX_norm"]
    train_X_norm = parameters_state["train_X_norm"]
    
    bo_loop_third_step_return = bo_loop_third_step(next_indices, train_indices, eval_spec_y, img, nextX_norm, train_X_norm)

    parameters_state["train_X"] = bo_loop_third_step_return["train_X"]
    parameters_state["train_X_norm"] = bo_loop_third_step_return["train_X_norm"]
    parameters_state["train_indices"] = bo_loop_third_step_return["train_indices"]
    
    aug_func_state["train_X"] = bo_loop_third_step_return["train_X"]
    aug_func_state["train_X_norm"] = bo_loop_third_step_return["train_X_norm"]
    aug_func_state["train_indices"] = bo_loop_third_step_return["train_indices"]
    aug_func_state["train_Y"] = bo_loop_third_step_return["train_Y"]
    aug_func_state["num_cols"] = bo_loop_third_step_return["num_cols"]
    aug_func_state["idx"] = bo_loop_third_step_return["idx"]
    aug_func_state["features"] = bo_loop_third_step_return["features"]
    aug_func_state["targets"] = bo_loop_third_step_return["targets"]
    aug_func_state["idx_x"] = bo_loop_third_step_return["idx_x"]
    aug_func_state["idx_y"] = bo_loop_third_step_return["idx_y"]
    aug_func_state["indices"] = bo_loop_third_step_return["indices"]
    aug_func_state["p"] = bo_loop_third_step_return["p"]
    
    return {"status": "bo_loop_third_step success", "bo_loop_counter": parameters_state["bo_loop_counter"], "switch_obj_index": parameters_state["switch_obj_index"]}

@app.post("/bo_loop_fourth_step_satisfied/")
async def bo_loop_fourth_step_satisfied_endpoint():
    global parameters_state
    global aug_func_state
    
    new_spec_x = parameters_state["new_spec_x"]
    new_spec_y = parameters_state["new_spec_y"]
    idx_y = aug_func_state["idx_y"]
    idx_x = aug_func_state["idx_x"]
    features = aug_func_state["features"]
    indices = aug_func_state["indices"]
    idx = aug_func_state["idx"]
    num_cols = aug_func_state["num_cols"]
    targets = aug_func_state["targets"]
    train_Y = aug_func_state["train_Y"]
    m = parameters_state["m"]
    var_params = parameters_state["var_params"]
    
    bo_fourth_step_satisfied_return = bo_loop_fourth_step_satisfied(new_spec_x, new_spec_y, idx_y, idx_x, features, indices, idx, num_cols, targets, train_Y, m, var_params)
    
    parameters_state["train_Y"] = bo_fourth_step_satisfied_return["train_Y"]
    parameters_state["m"] = bo_fourth_step_satisfied_return["m"]
    parameters_state["var_params"] = bo_fourth_step_satisfied_return["var_params"]
    
    print("train_X", parameters_state["train_X"])
    print("train_X_norm", parameters_state["train_X_norm"])
    print("train_indices", parameters_state["train_indices"])
    print("train_Y", parameters_state["train_Y"])
    print("var_params", parameters_state["var_params"])
    print("m", parameters_state["m"])
    
    return {"status": "bo_loop_fourth_step_satisfied success", "bo_loop_counter": parameters_state["bo_loop_counter"]}

@app.post("/bo_loop_fourth_step_unsatisfied_plot/")
async def bo_loop_fourth_step_unsatisfied_plot_endpoint():
    global parameters_state
    global aug_func_state
    
    idx_x = aug_func_state["idx_x"]
    idx_y = aug_func_state["idx_y"]
    new_spec_x = parameters_state["new_spec_x"]
    new_spec_y = parameters_state["new_spec_y"]
    img = parameters_state["img"]
    var_params = parameters_state["var_params"]
    
    bo_loop_fourth_step_unsatisfied_plot_return = bo_loop_fourth_step_unsatisfied_plot(idx_x, idx_y, new_spec_x, new_spec_y, img, var_params)

    plot = bo_loop_fourth_step_unsatisfied_plot_return["plot"]
    
    return {"status": "bo_loop_fourth_step_unsatisfied_plot success", "plot": plot}

@app.post("/bo_loop_fourth_step_unsatisfied_vote_process/")
async def bo_loop_fourth_step_unsatisfied_vote_process_endpoint(rating: Rating):
    global parameters_state
    global aug_func_state
    
    vote = rating.vote
    newspec_pref = rating.newspec_pref
    newspec_wt = rating.newspec_wt
    var_params = parameters_state["var_params"]
    new_spec_y = parameters_state["new_spec_y"]
    
    bo_loop_fourth_step_unsatisfied_vote_process_return = bo_loop_fourth_step_unsatisfied_vote_process(vote, newspec_pref, newspec_wt, var_params, new_spec_y)
    
    parameters_state["var_params"] = bo_loop_fourth_step_unsatisfied_vote_process_return["var_params"]
    aug_func_state["vote"] = bo_loop_fourth_step_unsatisfied_vote_process_return["vote"]
    
    return {"status": "bo_loop_fourth_step_unsatisfied_vote_process success", "wcount_good": parameters_state["wcount_good"]}

@app.post("/bo_loop_fourth_step_unsatisfied/")
async def bo_loop_fourth_step_unsatisfied_endpoint():
    global parameters_state
    global aug_func_state
    
    p = aug_func_state["p"]
    vote = aug_func_state["vote"]
    var_params = parameters_state["var_params"]
    features = aug_func_state["features"]
    indices = aug_func_state["indices"]
    idx = aug_func_state["idx"]
    num_cols = aug_func_state["num_cols"]
    targets = aug_func_state["targets"]
    train_Y = aug_func_state["train_Y"]
    new_spec_x = parameters_state["new_spec_x"]
    m = parameters_state["m"]
    
    bo_loop_fourth_step_unsatisfied_plot_return = bo_loop_fourth_step_unsatisfied(p, vote, var_params, features, indices, idx, num_cols, targets, train_Y, new_spec_x, m)
    
    parameters_state["train_Y"] = bo_loop_fourth_step_unsatisfied_plot_return["train_Y"]
    parameters_state["m"] = bo_loop_fourth_step_unsatisfied_plot_return["m"]
    parameters_state["var_params"] = bo_loop_fourth_step_unsatisfied_plot_return["var_params"]
    
    return {"status": "bo_loop_fourth_step_unsatisfied success", "bo_loop_counter": parameters_state["bo_loop_counter"]}

@app.post("/bo_loop_fifth_step/")
async def bo_loop_fifth_step_endpoint():
    global parameters_state
    
    train_X_norm = parameters_state["train_X_norm"]
    train_Y = parameters_state["train_Y"]
    
    bo_loop_fifth_step_return = bo_loop_fifth_step(train_X_norm, train_Y)
    
    parameters_state["gp_surro"] = bo_loop_fifth_step_return["gp_surro"]
    
    return {"status": "bo_loop_fifth_step success", "bo_loop_counter": parameters_state["bo_loop_counter"]}

@app.post("/bo_loop_automated/")
async def bo_loop_automated_endpoint():
    global parameters_state
    
    bo_loop_counter = parameters_state["bo_loop_counter"]
    num_bo = parameters_state["num_bo"]
    test_X_norm = parameters_state["test_X_norm"]
    indices = parameters_state["indices"]
    img = parameters_state["img"]
    test_X = parameters_state["test_X"]
    targets = parameters_state["targets"]
    vdc_vec = parameters_state["vdc_vec"]
    eval_spec_y = parameters_state["eval_spec_y"]
    gp_surro = parameters_state["gp_surro"]
    train_indices = parameters_state["train_indices"]
    train_Y = parameters_state["train_Y"]
    idx = parameters_state["idx"]
    train_X = parameters_state["train_X"]
    train_X_norm = parameters_state["train_X_norm"]
    var_params = parameters_state["var_params"]
    switch_obj_index = parameters_state["switch_obj_index"]
    m = parameters_state["m"]
    
    bo_loop_automated_return = bo_loop_automated(bo_loop_counter, num_bo, test_X_norm, indices, img, test_X, targets, vdc_vec, eval_spec_y, gp_surro, train_indices, train_Y, idx, train_X, train_X_norm, var_params, switch_obj_index, m)
    
    parameters_state["gp_surro"] = bo_loop_automated_return["gp_surro"]
    parameters_state["test_X_norm"] = bo_loop_automated_return["test_X_norm"]
    parameters_state["train_indices"] = bo_loop_automated_return["train_indices"]
    parameters_state["train_Y"] = bo_loop_automated_return["train_Y"]
    parameters_state["indices"] = bo_loop_automated_return["indices"]
    parameters_state["X_eval"] = bo_loop_automated_return["X_eval"]
    parameters_state["X_GP"] = bo_loop_automated_return["X_GP"]
    parameters_state["img"] = bo_loop_automated_return["img"]
    parameters_state["var_params"] = bo_loop_automated_return["var_params"]
    
    figures = bo_loop_automated_return["figures"]
    for fig in figures:
        parameters_state["bo_plots"].append(fig)
    
    location_plots = bo_loop_automated_return["location_plots"]
    
    return {"status": "bo_loop_automated success", "bo_loop_counter": parameters_state["bo_loop_counter"], "GP_figures": parameters_state["bo_plots"], "location_plots": location_plots}

@app.post("/bo_finish/")
async def bo_finish_endpoint():
    global parameters_state
    
    gp_surro = parameters_state["gp_surro"]
    test_X_norm = parameters_state["test_X_norm"]
    train_indices = parameters_state["train_indices"]
    train_Y = parameters_state["train_Y"]
    indices = parameters_state["indices"]
    X_eval = parameters_state["X_eval"]
    X_GP = parameters_state["X_GP"]
    img = parameters_state["img"]
    var_params = parameters_state["var_params"]
    bo_loop_counter = parameters_state["bo_loop_counter"]
    
    bo_finish_return = bo_finish(gp_surro, test_X_norm, train_indices, train_Y, indices, X_eval, X_GP, img, bo_loop_counter, var_params)
    
    parameters_state["optim_results"] = bo_finish_return["optim_results"]
    
    optim_results_str = "OK"
     
    return {"status": "bo_loop_last_step success", "bo_loop_counter": parameters_state["bo_loop_counter"], "optim_results": "OK"}