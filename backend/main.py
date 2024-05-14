from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import pickle

from dKLBO_functions.preprocess import preprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploading and preprocessing of the file.
processed_file_data = None
@app.post("/upload/")
async def process_file(file: UploadFile = File(...)):
    global processed_file_data
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
            return {"error": str(e)}
        
    import os
    os.remove("temp_large_file.p")
    
    processed_file_data = preprocess(uploaded_file)
    return {"status": "file upload success", "processed_file_data": processed_file_data}