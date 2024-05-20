from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pickle

from dKLBO_functions.preprocess import preprocess
from dKLBO_functions.initial_eval import initial_eval_loop_plot, initial_eval_vote_process

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:5173"],  # Allow frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store the return values of the functions
class NumStart(BaseModel):
    num_start: int

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
    "new_spec_y": None,
    "pref": None,
    "wcount_good": None,
    "target_func": None,
    "initial_eval_loop_counter": None,
    "plot_history": []
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
    parameters_state["amp_masked"] = preprocess_return["amp_masked"]
    parameters_state["train_indices"] = preprocess_return["train_indices"]
    parameters_state["m"] = preprocess_return["m"]
    parameters_state["points_measured"] = preprocess_return["points_measured"]
    parameters_state["last_points_measured"] = preprocess_return["last_points_measured"]
    parameters_state["IV"] = preprocess_return["IV"]
    parameters_state["init_spec"] = preprocess_return["init_spec"]
    parameters_state["eval_spec_y"] = preprocess_return["eval_spec_y"]
    parameters_state["pref"] = preprocess_return["pref"]
    parameters_state["wcount_good"] = preprocess_return["wcount_good"]
    parameters_state["target_func"] = preprocess_return["target_func"]
    parameters_state["initial_eval_loop_counter"] = preprocess_return["initial_eval_loop_counter"]
    
    # print(preprocess_return)
    return {"status": "file upload success", "num_start": parameters_state["num_start"]}
    
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
    parameters_state["new_spec_y"] = initial_eval_loop_return["new_spec_y"]
    plot_data = initial_eval_loop_return["plot_data"]
    plot_history_item = {"plot_data": plot_data, "rating": None}
    parameters_state["plot_history"].append(plot_history_item)
    
    
    return {"status": "initial_eval_loop success", "plot_data": plot_data, "current_wcount_good": parameters_state["wcount_good"], "plot_history": parameters_state["plot_history"], "num_start": parameters_state["num_start"]}

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
    
    return {"status": "initial_eval_vote_process success", "initial_eval_loop_counter": parameters_state["initial_eval_loop_counter"]}