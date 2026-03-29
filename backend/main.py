from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import torch.nn as nn
import joblib
import pandas as pd
import numpy as np
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model definition (must match training)
class EfficiencyNet(nn.Module):
    def __init__(self, input_size):
        super(EfficiencyNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.net(x)

# Global variables
model = None
preprocessor = None

@app.on_event("startup")
def load_assets():
    global model, preprocessor
    model_path = "model/efficiency_model.pth"
    preprocessor_path = "model/preprocessor.pkl"
    
    if os.path.exists(model_path) and os.path.exists(preprocessor_path):
        preprocessor = joblib.load(preprocessor_path)
        # We need the input dimension from the preprocessor output
        # Let's use a dummy transform to get the shape if needed, 
        # or just wait for the first request if we don't know it.
        # But we can infer it if we have the preprocessor object.
        print("Preprocessor loaded.")
    else:
        print("Model or preprocessor not found in 'model/' folder.")

class ManufacturingData(BaseModel):
    Injection_Temperature: float
    Injection_Pressure: float
    Cycle_Time: float
    Cooling_Time: float
    Material_Viscosity: float
    Ambient_Temperature: float
    Machine_Age: float
    Operator_Experience: float
    Maintenance_Hours: float
    Shift: str
    Machine_Type: str
    Material_Grade: str
    Day_of_Week: str
    Temperature_Pressure_Ratio: float
    Total_Cycle_Time: float
    Machine_Utilization: float
    Parts_Per_Hour: float

@app.post("/predict")
def predict(data: ManufacturingData):
    global model, preprocessor
    if preprocessor is None:
        raise HTTPException(status_code=503, detail="Assets not loaded. Check model/ folder.")
    
    # Convert input to DataFrame for preprocessor
    input_df = pd.DataFrame([data.dict()])
    
    # Preprocess
    input_processed = preprocessor.transform(input_df)
    input_tensor = torch.FloatTensor(input_processed)
    
    # Initialize model if not already (using processed dimension)
    if model is None:
        input_dim = input_processed.shape[1]
        model = EfficiencyNet(input_dim)
        model_path = "model/efficiency_model.pth"
        if os.path.exists(model_path):
            model.load_state_dict(torch.load(model_path))
            model.eval()
        else:
            raise HTTPException(status_code=503, detail="Model file missing.")

    # Inference
    with torch.no_grad():
        prediction = model(input_tensor).item()
    
    return {
        "predicted_efficiency_score": prediction
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
