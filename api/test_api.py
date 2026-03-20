import requests
import json

data = {
    'Age': 65,
    'Gender': 'Male',
    'BMI': 32,
    'Smoking': 'Yes',
    'BloodPressure': 'High',
    'Diabetes': 1,
    'ChronicCond_Heartfailure': 1,
    'ChronicCond_Cancer': 0,
    'Respiratory_Issues': 'Yes',
    'Children': 1,
    'ClaimHistory_Frequency': '3+',
    'HospitalizationHistory': 'Yes'
}

try:
    response = requests.post('http://localhost:5000/predict', json=data)
    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error testing API: {e}")
