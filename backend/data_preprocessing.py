import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

def generate_synthetic_data(num_samples=5000):
    """Generates a realistic synthetic dataset for health risk prediction."""
    np.random.seed(42)
    
    # Base features
    age = np.random.randint(18, 85, size=num_samples)
    bmi = np.random.normal(26.5, 5.0, size=num_samples)
    bmi = np.clip(bmi, 15, 50)
    
    # Categorical/Binary features
    gender = np.random.choice(['Male', 'Female'], size=num_samples)
    smoking = np.random.choice(['Yes', 'No'], size=num_samples, p=[0.2, 0.8])
    blood_pressure = np.random.choice(['Normal', 'High', 'Low'], size=num_samples, p=[0.6, 0.3, 0.1])
    
    # Conditions (correlations intentionally added to make it learnable)
    # Higher age/bmi/smoking correlate with higher probabilities
    prob_diabetes = np.where(age > 45, 0.25, 0.05) + np.where(bmi > 30, 0.15, 0)
    diabetes = np.random.binomial(1, np.clip(prob_diabetes, 0, 1))
    
    prob_heart = np.where(age > 50, 0.2, 0.02) + (diabetes * 0.15) + np.where(blood_pressure == 'High', 0.1, 0)
    heart_disease = np.random.binomial(1, np.clip(prob_heart, 0, 1))
    
    prob_cancer = np.where(age > 60, 0.1, 0.01) + np.where(smoking == 'Yes', 0.15, 0)
    cancer = np.random.binomial(1, np.clip(prob_cancer, 0, 1))
    
    resp_risk = np.random.choice(['Yes', 'No'], size=num_samples, p=[0.15, 0.85])
    prob_resp = np.where(smoking == 'Yes', 0.6, 0.05)
    respiratory_issues = np.random.binomial(1, np.clip(prob_resp, 0, 1))
    respiratory_issues_str = np.where(respiratory_issues == 1, 'Yes', 'No')

    children = np.random.randint(0, 5, size=num_samples)
    
    # Historical Data
    claim_history = np.random.choice(['0', '1-2', '3+'], size=num_samples, p=[0.5, 0.35, 0.15])
    hospitalization = np.random.choice(['Yes', 'No'], size=num_samples, p=[0.2, 0.8])

    df = pd.DataFrame({
        'Age': age,
        'Gender': gender,
        'BMI': bmi,
        'Smoking': smoking,
        'BloodPressure': blood_pressure,
        'Diabetes': diabetes,
        'ChronicCond_Heartfailure': heart_disease,
        'ChronicCond_Cancer': cancer,
        'Respiratory_Issues': respiratory_issues_str,
        'Children': children,
        'ClaimHistory_Frequency': claim_history,
        'HospitalizationHistory': hospitalization
    })
    
    # Introduce some missing values to test imputation
    mask = np.random.rand(len(df)) < 0.05
    df.loc[mask, 'BMI'] = np.nan
    mask = np.random.rand(len(df)) < 0.02
    df.loc[mask, 'BloodPressure'] = np.nan
    
    # Define Target: RiskCategory based on somewhat complex logic
    # We want a continuous risk score first
    risk_score = (age / 100) * 0.3 + (bmi / 50) * 0.2
    risk_score += np.where(smoking == 'Yes', 0.15, 0)
    risk_score += np.where(diabetes == 1, 0.1, 0)
    risk_score += np.where(heart_disease == 1, 0.15, 0)
    risk_score += np.where(cancer == 1, 0.15, 0)
    risk_score += np.where(hospitalization == 'Yes', 0.1, 0)
    
    df['RiskCategory'] = pd.cut(risk_score, bins=[0, 0.4, 0.65, float('inf')], labels=['Low Risk', 'Medium Risk', 'High Risk'])
    
    return df

class DataPreprocessor:
    def __init__(self):
        self.num_imputer = SimpleImputer(strategy='median')
        self.cat_imputer = SimpleImputer(strategy='most_frequent')
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
        self.numeric_features = ['Age', 'BMI', 'Children']
        self.categorical_features = ['Gender', 'Smoking', 'BloodPressure', 'Respiratory_Issues', 
                                     'ClaimHistory_Frequency', 'HospitalizationHistory']
        
    def fit_transform(self, df):
        # Impute missing values
        df[self.numeric_features] = self.num_imputer.fit_transform(df[self.numeric_features])
        df[self.categorical_features] = self.cat_imputer.fit_transform(df[self.categorical_features])
        
        # Scale numeric
        df[self.numeric_features] = self.scaler.fit_transform(df[self.numeric_features])
        
        # Encode categorical
        for col in self.categorical_features:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.label_encoders[col] = le
            
        return df
        
    def transform(self, df):
        df_copy = df.copy()
        df_copy[self.numeric_features] = self.num_imputer.transform(df_copy[self.numeric_features])
        df_copy[self.categorical_features] = self.cat_imputer.transform(df_copy[self.categorical_features])
        
        df_copy[self.numeric_features] = self.scaler.transform(df_copy[self.numeric_features])
        
        for col in self.categorical_features:
            # Handle unseen labels by mapping to a known mode class
            le = self.label_encoders[col]
            classes = list(le.classes_)
            df_copy[col] = df_copy[col].apply(lambda x: x if x in classes else classes[0])
            df_copy[col] = le.transform(df_copy[col])
            
        return df_copy
