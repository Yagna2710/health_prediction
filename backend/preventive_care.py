def generate_preventive_care(risk_level, data):
    """
    Maps health risks to preventive steps. Generates actionable checkup 
    suggestions and lifestyle tips.
    """
    bmi = float(data.get('BMI', 25.0))
    diabetes = int(data.get('Diabetes', 0))
    heart = int(data.get('ChronicCond_Heartfailure', 0))
    resp = data.get('Respiratory_Issues', 'No')
    
    actions = []
    screenings = ['Annual General Check-up']
    lifestyle = []
    
    # Specific targeted logic
    if bmi > 30:
        actions.append("Initiate structured weight management program.")
        screenings.append("Bariatric risk assessment.")
        lifestyle.append("Caloric deficit diet, 30m daily cardiovascular activity.")
        
    if diabetes == 1:
        actions.append("Enroll in diabetic care registry.")
        screenings.append("HbA1c Blood Sugar Monitoring (every 3 months).")
        lifestyle.append("Strict low-glycemic index foods.")
        
    if heart == 1 or data.get('BloodPressure') == 'High':
        actions.append("Hypertension & Cardiovascular management tracking.")
        screenings.append("ECG and Lipid Profile testing.")
        lifestyle.append("Low sodium DASH diet, manage stress/salt intake.")
        
    if resp == 'Yes' or data.get('Smoking') == 'Yes':
         actions.append("Pulmonary rehabilitation or smoking cessation counseling.")
         screenings.append("Pulmonary Function Tests (Spirometry).")
         lifestyle.append("Eliminate tobacco usage, avoid severe air pollution zones.")
         
    if risk_level == 'High Risk':
        lifestyle.append("Consider speaking to a dedicated wellness coach.")

    return {
        'preventive_actions': actions,
        'health_recommendations_checkups': screenings,
        'lifestyle_improvement_tips': lifestyle if lifestyle else ["Maintain current healthy routine."]
    }
