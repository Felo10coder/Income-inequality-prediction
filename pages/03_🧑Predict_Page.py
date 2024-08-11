import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import csv

# Define your backend URL
backend_url = "http://127.0.0.1:8000"

# Page configuration
st.set_page_config(page_title='Income Prediction App', page_icon='📊', layout='wide')

st.title('Income Prediction Application')

st.markdown("""
This application allows you to input various details and predict the income level. 
Please enter the required features in the form below and click 'Submit' to get the prediction.
""")

def show_form():
    st.header('Input Features 📝')
    with st.form('input-feature'):
        # Define columns for input fields
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            age = st.number_input('Age', min_value=0, max_value=90, value=30)
            gender = st.selectbox('Gender', options=['Female', 'Male'])
            education = st.selectbox('Education', options=[
                'High school graduate', '12th grade no diploma', 'Children',
                'Bachelors degree(BA AB BS)', '7th and 8th grade', '11th grade', '9th grade',
                'Masters degree(MA MS MEng MEd MSW MBA)', '10th grade',
                'Associates degree-academic program', '1st 2nd 3rd or 4th grade',
                'Some college but no degree', 'Less than 1st grade',
                'Associates degree-occup /vocational',
                'Prof school degree (MD DDS DVM LLB JD)', '5th or 6th grade',
                'Doctorate degree(PhD EdD)'
            ])
            income_class = st.selectbox('income_class', options=[' Federal government', ' Private', ' Local government',
                 ' Self-employed-incorporated', ' Self-employed-not incorporated',
                ' State government', ' Without pay', ' Never worked'
            ])
            marital_status = st.selectbox('Marital Status', options=[
                'Widowed', 'Never married', 'Married-civilian spouse present', 'Divorced',
                'Married-spouse absent', 'Separated', 'Married-A F spouse present'
            ])
            race = st.selectbox('Race', options=[
                'White', 'Black', 'Asian or Pacific Islander', 'Amer Indian Aleut or Eskimo',
                'Other'
            ])
            is_hispanic = st.selectbox('is_hispanic', options=[
                'All other', 'Mexican-American', 'Central or South American',
                'Mexican (Mexicano)', 'Puerto Rican', 'Other Spanish', 'Cuban', 'Do not know',
                'Chicano'
            ])
            employment_commitment = st.selectbox('employment_commitment', options=[
                'Not in labor force', 'Children or Armed Forces', 'Full-time schedules',
                'PT for econ reasons usually PT', 'Unemployed full-time',
                'PT for non-econ reasons usually FT', 'PT for econ reasons usually FT',
                'Unemployed part- time'
            ])
        
        with col2:
            employment_stat = st.selectbox('employment_stat', options=[0, 1, 2])
            wage_per_hour = st.number_input('wage_per_hour', min_value=0, max_value=1949)
            is_labor_union = st.selectbox('is_labor_union', options=[' No', 'Same'])
            working_week_per_year = st.number_input(' working_week_per_year', min_value=0, max_value=52, value=40)
            industry_code = st.selectbox('industry_code ', options=list(range(52)))
            occupation_code = st.number_input('occupation_code', min_value=0, max_value=46, step=1)
            total_employed = st.selectbox(' total_employed', options=[0, 1, 2, 3, 4, 5, 6])
        
        with col3:
            household_summary = st.selectbox('household_summary', options=[
                'Householder', 'Child 18 or older', 'Child under 18 never married',
                'Spouse of householder', 'Nonrelative of householder',
                'Other relative of householder', 'Group Quarters- Secondary individual',
                'Child under 18 ever married'
            ])
            vet_benefit = st.selectbox('vet_benefit', options=[0, 1, 2])
            tax_status = st.selectbox('tax_status', options=[
                'Head of household', 'Single', 'Nonfiler', 'Joint both 65+',
                'Joint both under 65', 'Joint one under 65 & one 65+'
            ])
            stocks_status = st.number_input('stocks_status', min_value=0, max_value=5531, step=1)
            citizenship = st.selectbox('citizenship', options=[
                'Native', 'Foreign born- Not a citizen of U S',
                'Foreign born- U S citizen by naturalization',
                'Native- Born abroad of American Parent(s)',
                'Native- Born in Puerto Rico or U S Outlying'
            ])
        
        with col4:
            mig_year = st.selectbox('mig_year', options=[94, 95])
            country_of_birth_own = st.selectbox('country_of_birth_own', options=[
                'US', 'El-Salvador', 'Mexico', 'Philippines', 'Cambodia', 'China',
                'Hungary', 'Puerto-Rico', 'England', 'Dominican-Republic', 'Japan', 'Canada',
                'Ecuador', 'Italy', 'Cuba', 'Peru', 'Taiwan', 'South Korea', 'Poland',
                'Nicaragua', 'Germany', 'Guatemala', 'India', 'Ireland', 'Honduras', 'France',
                'Trinadad&Tobago', 'Thailand', 'Iran', 'Vietnam', 'Portugal', 'Laos', 'Panama',
                'Scotland', 'Columbia', 'Jamaica', 'Greece', 'Haiti', 'Yugoslavia',
                'Outlying-U S (Guam USVI etc)', 'Holand-Netherlands', 'Hong Kong'
            ])
            importance_of_record = st.number_input('importance_of_record', min_value=791.61, max_value=1779.74, step=0.1)
        
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            input_data = {
                'age': age,
                'gender': gender,
                'education': education,
                'income_class': income_class,
                'marital_status': marital_status,
                'race': race,
                'is_hispanic': is_hispanic,
                'employment_commitment': employment_commitment,
                'employment_stat': employment_stat,
                'wage_per_hour': wage_per_hour,
                'is_labor_union': is_labor_union,
                'working_week_per_year': working_week_per_year,
                'industry_code': industry_code,
                'occupation_code': occupation_code,
                'total_employed': total_employed,
                'household_summary': household_summary,
                'vet_benefit': vet_benefit,
                'tax_status': tax_status,
                'stocks_status': stocks_status,
                'citizenship': citizenship,
                'mig_year': mig_year,
                'country_of_birth_own' : country_of_birth_own,
                'importance_of_record': importance_of_record
            }
            
            response = requests.post(f"{backend_url}/predict_income", json=input_data)
            
            if response.status_code == 200:
                prediction = response.json()['prediction']
                st.write(f"**Prediction:** The model predicts that the individual earns {prediction}.")
                
                # Save prediction to CSV
                log_prediction(input_data, prediction)
                
            else:
                st.error("Error: Unable to get prediction from API")

def log_prediction(features, prediction):
    filename = 'prediction_history.csv'
    fieldnames = features.keys()
    fieldnames = list(fieldnames) + ['prediction', 'timestamp']
    
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            file_exists = file.tell() != 0
            
            if not file_exists:
                writer.writeheader()
                
            features['prediction'] = prediction
            features['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow(features)
    
    except Exception as e:
        st.error(f"Error logging prediction: {e}")

show_form()

st.subheader('Prediction History 📜')

try:
    # Display the prediction history
    history_df = pd.read_csv('prediction_history.csv')
    st.write(history_df)
except FileNotFoundError:
    st.write("No prediction history found.")