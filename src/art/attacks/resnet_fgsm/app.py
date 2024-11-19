from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import json

app = FastAPI()

class AttackRequest(BaseModel):
    model: str
    attack: str
    epsilon: float

@app.post("/resnet-attack/")
def run_attack(request: AttackRequest):
    script_name = f"{request.model}_{request.attack}.py"
    epsilon = request.epsilon

    if not os.path.exists(script_name):
        raise HTTPException(status_code=404, detail="Model script not found")

    command = ["python3", script_name, "--eps", str(epsilon)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error running script: {e.stderr}")

    try:
        # Parse the JSON output from the script
        results = json.loads(output)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to decode script output")

    return results