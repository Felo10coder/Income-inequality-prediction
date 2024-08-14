import streamlit as st

# Page setup
st.set_page_config(page_title='Income Prediction App', page_icon='🏠', layout='wide')

# Set up page title
st.title('Income Prediction App')

# Create columns
col1, col2 = st.columns(2)

with col1:
    st.subheader('About the App')
    st.markdown("""
    This app predicts if an individual earns above or below an income threshold based on their characteristics. 
    Utilize advanced machine learning models for accurate predictions instantly.

    To use the app, enter your details on the Predict page and click the "Predict" button.
    """)

with col2:
    st.subheader('About the Models')
    st.markdown("""
    This app uses state-of-the-art classifiers: XGBClassifier and RandomForestClassifier, trained on extensive data for precise income predictions.

    **Evaluation Metric: F1 Score**  
    - **XGBClassifier:** 97.4  
    - **RandomForestClassifier:** 97.3  
    """)

# Footer
st.markdown("""
    <hr>
    <footer style="text-align: center; margin-top: 50px;">
        <p style="font-size: 0.9rem; color: #AAB7B8;">&copy; 2024 Income Prediction App. All rights reserved.</p>
    </footer>
""", unsafe_allow_html=True)
