import os
import pickle
import pandas as pd
from data_preprocessing import DataPreprocessor

# Load model pipeline once
PIPELINE_PATH = os.path.join(os.path.dirname(__file__), 'health_rf_pipeline.pkl')
try:
    with open(PIPELINE_PATH, 'rb') as f:
        pipeline = pickle.load(f)
        MODEL = pipeline['model']
        PREPROCESSOR = pipeline['preprocessor']
        FEATURES = pipeline['features']
        print("ML Pipeline loaded successfully.")
except Exception as e:
    print(f"Error loading model pipeline: {e}")
    MODEL = None
    PREPROCESSOR = None
    FEATURES = None

def get_prediction(data):
    """
    Takes raw user input dictionary, maps it to the expected schema,
    preprocesses it, and returns the predicted probability and category.
    """
    if not MODEL or not PREPROCESSOR:
        raise ValueError("Model pipeline is not initialized.")
        
    # Map input raw data to DataFrame schema
    # Defaults handled in the API layer, but we ensure all expected keys exist.
    row = {
        'Age': int(data.get('Age', 30)),
        'Gender': data.get('Gender', 'Male'),
        'BMI': float(data.get('BMI', 25.0)),
        'Smoking': data.get('Smoking', 'No'),
        'BloodPressure': data.get('BloodPressure', 'Normal'),
        'Diabetes': int(data.get('Diabetes', 0)),
        'ChronicCond_Heartfailure': int(data.get('ChronicCond_Heartfailure', 0)),
        'ChronicCond_Cancer': int(data.get('ChronicCond_Cancer', 0)),
        'Respiratory_Issues': data.get('Respiratory_Issues', 'No'),
        'Children': int(data.get('Children', 0)),
        'ClaimHistory_Frequency': data.get('ClaimHistory_Frequency', '0'),
        'HospitalizationHistory': data.get('HospitalizationHistory', 'No')
    }
    
    df = pd.DataFrame([row])
    
    # Preprocess
    df_processed = PREPROCESSOR.transform(df)
    
    # Predict
    # predict_proba returns probability for each class based on training labels:
    # Let's say classes are ['High Risk', 'Low Risk', 'Medium Risk']
    proba_array = MODEL.predict_proba(df_processed)[0]
    class_idx = MODEL.predict(df_processed)[0]
    
    # Determine the "Risk Probability" generally representing the likelihood of Medium/High
    # We will pick the max probability of the assigned class, or construct a combined score.
    # To keep it intuitive for the front end, risk_probability = prob of assigned class if High/Medium, 
    # or (1 - prob(Low Risk)). Let's just use the max probability of any risk class for now.
    
    # Identify index of 'Low Risk' to compute an 'overall risk' metric
    classes = list(MODEL.classes_)
    if 'Low Risk' in classes:
        prob_low = proba_array[classes.index('Low Risk')]
        overall_risk_prob = 1.0 - prob_low
    else:
        # Fallback if classes somehow differ
        overall_risk_prob = max(proba_array)
        
    # Determine the critical key factors driving this prediction heuristically, 
    # since getting feature importance per prediction requires Shapley values.
    key_factors = []
    if row['Smoking'] == 'Yes': key_factors.append("Smoking")
    if row['BMI'] > 30: key_factors.append("High BMI")
    if row['BloodPressure'] == 'High': key_factors.append("Hypertension")
    if row['Diabetes'] == 1: key_factors.append("Diabetes")
    if row['ChronicCond_Heartfailure'] == 1: key_factors.append("Heart Disease History")
    if row['ChronicCond_Cancer'] == 1: key_factors.append("Cancer History")
    if row['Age'] > 55: key_factors.append("Age")
    
    if len(key_factors) == 0:
        key_factors.append("Healthy Lifestyle")
        
    return {
        'risk_level': class_idx,
        'risk_probability': round(float(overall_risk_prob), 2),
        'key_factors': key_factors[:3] # Return top 3 factors
    }
