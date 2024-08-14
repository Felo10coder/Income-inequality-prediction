from fastapi import FastAPI, Query
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import numpy as np

app = FastAPI()
# loading models and encoder
random = joblib.load('../toolkit/random.joblib')  
xgb = joblib.load('../toolkit/xgb.joblib')
encoder = joblib.load('../toolkit/encoder.joblib')


class DfFeatures(BaseModel):
    age: int
    gender: object
    education: object
    income_class: object
    marital_status: object
    race: object
    is_hispanic: object
    employment_commitment: object
    employment_stat: int
    wage_per_hour: int
    is_labor_union: object
    working_week_per_year: int
    industry_code: int
    occupation_code: int
    total_employed: int
    household_summary: object
    vet_benefit: int
    tax_status: object
    stocks_status: int
    citizenship: object
    mig_year: int
    country_of_birth_own: object
    importance_of_record: float
@app.get('/')
def status_check(
    title: str = Query('Income Prediction API', title='Project Title', description='Title of the project'),
):
    status_message = {
        'api_name': 'Income Prediction API',
        'description': '''The project focuses on leveraging machine learning to predict whether individuals in developing
        nations earn above or below a specific income threshold,
        aiming to address the pressing issue of income inequality mostly witnessed in developing nations.''',
        'status': 'API is online and functioning correctly.',
        'models_loaded': {
            'random': 'loaded',
            'xgb': 'loaded',
            'encoder': 'loaded'
        }
    }
    return status_message

@app.post('/predict_income')
def predict_income(data: DfFeatures, model: str = Query('xgb', enum=['random','xgb'])):
    df = pd.DataFrame([data.model_dump()])

    # Select the model based on the query parameter
    if model == 'random':
        prediction = random.predict(df)
        probability = random.predict_proba(df)
    elif model == 'xgb':
        prediction = xgb.predict(df)
        probability = xgb.predict_proba(df)
    
    prediction = int(prediction[0])
    prediction = encoder.inverse_transform([prediction])[0]
    probability = probability[0]

    return {
        'model_used': model,
        'prediction': prediction,
        'probability': f'The probability of the prediction is {probability[0]:.2f}'
    }