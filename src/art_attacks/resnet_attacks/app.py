from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import os
import json
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AttackRequest(BaseModel):
    model: str
    attack: str
    epsilon: Optional[float] = None
    eps_step: Optional[float] = None
    max_iter: Optional[int] = None


@app.post("/resnet-attack/")
def run_attack(request: AttackRequest):
    '''
    Function to serve requested attack to front end. Runs attack script
    by translating drop down menu selections to command line arguments.
    '''
    script_name = f"{request.model}_attacks.py"
    epsilon = request.epsilon

    if not os.path.exists(script_name):
        raise HTTPException(status_code=404, detail="Model script not found")
    
    command = ["python3", script_name]

    if request.attack == "fgsm":
        command.append("--fgsm")
    elif request.attack == "pgd":
        command.append("--pgd")
    elif request.attack == "deepfool":
        command.append("--deepfool")
    elif request.attack == "square":
        command.append("--square")
    else:
        raise HTTPException(status_code=400, detail="Invalid attack type")

    if request.epsilon is not None:
        command.extend(["--eps", str(request.epsilon)])
    if request.eps_step is not None:
        command.extend(["--eps_step", str(request.eps_step)])
    if request.max_iter is not None:
        command.extend(["--max_iter", str(request.max_iter)])

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error running script: {e.stderr}")

    try:
        results = json.loads(output)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to decode script output")

    return results

@app.get("/get-file/")
def get_file(file_path: str):
    """
    Function to serve image of sample before and after adversarial perturbation.
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=os.path.basename(file_path))