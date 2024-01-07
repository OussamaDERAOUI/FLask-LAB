import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pickle
import numpy as np

# Load the trained model and preprocessing transformations
with open('preprocessing_transformations.pkl', 'rb') as file:
    preprocessing_pipeline = pickle.load(file)

model = pickle.load(open('svm_model.pkl', 'rb'))

class PredictionRequest(BaseModel):
    gender: float
    year: float
    marital: float
    anxiety: float
    panic: float
    treatment: float
    mingpa: float
    maxgpa: float

app = FastAPI()

@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        input_data = np.array([[request.gender, request.year, request.marital,
                                request.anxiety, request.panic, request.treatment,
                                request.mingpa, request.maxgpa]])
        

        
        # Make a prediction using the loaded model
        prediction = model.predict(input_data)[0]
        
        return {"prediction": str(prediction)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Prediction failed: {str(e)}"})

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)
