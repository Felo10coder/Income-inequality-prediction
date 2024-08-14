import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Set page configuration
st.set_page_config(page_title='Bulk Predict Page', page_icon='📜', layout='wide')

# Set up page title
st.title('Bulk Prediction Page')

# Load models
@st.cache_resource(show_spinner='Models Loading ...')
def load_models():
    xgb = joblib.load('./toolkit/xgb.joblib')
    rfc = joblib.load('./toolkit/random.joblib')
    encoder = joblib.load('./toolkit/encoder.joblib')
    return xgb, rfc, encoder

# Load the models
xgb_model, rfc_model, label_encoder = load_models()

# Prediction function
def predict_bulk(model, data):
    predictions = model.predict(data)
    probabilities = model.predict_proba(data)[:, 1]  # Probabilities for the positive class
    return predictions, probabilities

# Data cleaning function
def clean_data(data):
    # Assuming the cleaning steps are defined here
    # Example:
    # data = data.dropna()
    # data = data.drop_duplicates()
    
    # Check if 'ID' column exists, if not create one
    if 'ID' not in data.columns:
        data['ID'] = range(1, len(data) + 1)
    
    return data

# User upload file section
st.subheader('Upload your CSV file for bulk prediction')
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    # Read the uploaded file
    user_data = pd.read_csv(uploaded_file)
    
    # Clean the data
    cleaned_data = clean_data(user_data)
    
    # Display cleaned data
    st.subheader('Data Loaded for Prediction')
    st.write(cleaned_data)

    # Select model for prediction
    model_choice = st.selectbox('Choose a model for prediction', ('XGBoost', 'Random Forest'))
    model = xgb_model if model_choice == 'XGBoost' else rfc_model

    # Separate ID column and features
    ids = cleaned_data['ID']
    features = cleaned_data.drop('ID', axis=1)

    # Make predictions
    predictions, probabilities = predict_bulk(model, features)

    # Inverse encoding for predictions
    predictions = label_encoder.inverse_transform(predictions)

    # Prepare results DataFrame
    results_df = pd.DataFrame({
        'Prediction': predictions,
        'Probability': probabilities
    })

    # Display results
    st.subheader('Prediction Results')
    full_results = pd.concat([cleaned_data, results_df], axis=1)
    st.write(full_results)

    # Convert full results to CSV
    csv_data = full_results.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download predictions as CSV",
        data=csv_data,
        file_name="bulk_predictions.csv",
        mime="text/csv",
    )
