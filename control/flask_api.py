from fastapi.templating import Jinja2Templates
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open('svm_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load the preprocessing transformations
with open('preprocessing_transformations.pkl', 'rb') as file:
    preprocessing_pipeline = pickle.load(file)

templates = Jinja2Templates(directory="templates/")

"""@app.route('/')
def home():
    return 'ML model for depression prediction'"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve feature values from the request
    form_data = request.form
    gender = float(form_data["gender"])
    year = float(form_data["year"])
    marital = float(form_data["marital"])
    anxiety = float(form_data["anxiety"])
    panic = float(form_data["panic"])
    treatement = float(form_data["treatement"])
    mingpa = float(form_data["mingpa"])
    maxgpa = float(form_data["maxgpa"])

    # Make a prediction using the loaded model
    output = model.predict([[gender, year, marital, anxiety, panic, treatement, mingpa, maxgpa]])[0]
    if output == 1:
        output = "DEPRESSION POSITIVE"
    else:
        output = "NO DEPRESSION"
    return render_template('index.html', prediction=output)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)