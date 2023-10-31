import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
import pickle
import numpy as np

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

@app.get("/")
async def home(request: Request):
    #return templates.TemplateResponse("index.html", {"request": request})
    return {'ML model for furniture prediction'}

@app.post("/predict")
async def predict(request: Request):
    # Retrieve feature values from the request
    form_data = await request.form()
    category = float(form_data["category"])
    sellable_online = float(form_data["sellable_online"])
    other_colors = float(form_data["other_colors"])
    depth = float(form_data["depth"])
    height = float(form_data["height"])
    width = float(form_data["width"])

    # Make a prediction using the loaded model
    prediction = model.predict([[category, sellable_online, other_colors, depth, height, width]])[0]
    output = round(prediction,2)
    #return templates.TemplateResponse("index.html", {"request": request, "prediction": output})
    return ({"prediction": str(output)})

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.1.0.0", port=8080, reload=True)









"""
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
app = FastAPI()
class iris(BaseModel):
    a:float
    b:float
    c:float
    d:float

from sklearn.linear_model import LogisticRegression
import pandas as pd
import pickle

#we are loading the model using pickle
model = pickle.load(open('model_iris', 'rb'))

@app.get("/")
def home():
    return {'ML model for Iris prediction'}
@app.post('/make_predictions')
async def make_predictions(features: iris):
    return({"prediction":str(model.predict([[features.a,features.b,features.c,features.d]])[0])})

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
"""