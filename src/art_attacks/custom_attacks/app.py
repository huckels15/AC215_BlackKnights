from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.cloud import storage
import os
import shutil
import numpy as np
from typing import Optional, List
import zipfile

# Google Cloud Storage configuration
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/secrets.json'
GCS_BUCKET_NAME = "custom-attacks"

# FastAPI app setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class AttackRequest(BaseModel):
    model: str
    attack: str
    epsilon: Optional[float] = None
    eps_step: Optional[float] = None
    max_iter: Optional[int] = None

def upload_file_to_gcs(bucket_name: str, local_file_path: str, gcs_blob_path: str):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(gcs_blob_path)
    blob.upload_from_filename(local_file_path)

@app.post("/upload-model/")
async def upload_model(file: UploadFile = File(...)):
    """
    Upload model to local storage and then to GCS.
    """
    model_path = "./uploads/"
    os.makedirs(model_path, exist_ok=True)

    local_model_file = os.path.join(model_path, file.filename)
    with open(local_model_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    gcs_folder = f"run/"
    gcs_filepath = os.path.join(gcs_folder, file.filename)
    upload_file_to_gcs(GCS_BUCKET_NAME, local_model_file, gcs_filepath)
    return {"message": f"Model uploaded to {gcs_folder}"}

@app.post("/upload-directory/")
async def upload_directory(file: List[UploadFile] = File(...)):
    """
    Upload zip, unzip locally, and upload the unzipped files with directory structure to GCS.
    """
    temp_path = "./temp_model"
    os.makedirs(temp_path, exist_ok=True)

    # Save uploaded zip file locally
    zip_path = os.path.join(temp_path, file[0].filename)
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file[0].file, buffer)

    # Unzip the file locally
    extract_path = os.path.join(temp_path, "unzipped")
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Upload each file and folder in the extracted zip to GCS
    gcs_folder = "run/"
    for root, dirs, files in os.walk(extract_path):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(local_file_path, extract_path)
            gcs_file_path = os.path.join(gcs_folder, relative_path)
            upload_file_to_gcs(GCS_BUCKET_NAME, local_file_path, gcs_file_path)

    # Clean up local temp files after uploading
    shutil.rmtree(temp_path)

    return {"message": f"Contents uploaded to GCS with directory structure under '{gcs_folder}'"}

@app.post("/predict/")
async def predict(payload: dict):
    """
    Perform predictions using the uploaded model and dataset.
    """
    instances = payload.get("instances")
    if not instances or not isinstance(instances, list) or len(instances) == 0:
        raise HTTPException(status_code=400, detail="Invalid payload format. Expected 'instances' as a non-empty list.")

    instance = instances[0]

    try:
        request = AttackRequest(**instance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid instance format: {str(e)}")

    # Example: Use GCS paths for the uploaded model and dataset
    model_gcs_path = f"gs://{GCS_BUCKET_NAME}/run/"
    dataset_gcs_path = f"gs://{GCS_BUCKET_NAME}/run//"

    # Replace this logic with your actual prediction script
    result = {
        "model": model_gcs_path,
        "dataset": dataset_gcs_path,
        "attack": request.attack,
        "epsilon": request.epsilon,
        "status": "Prediction completed"
    }

    return {"result": result}
