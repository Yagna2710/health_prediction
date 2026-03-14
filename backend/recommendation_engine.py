def generate_recommendation(risk_score, risk_prob, data):
    """
    Suggests the best insurance plan type, coverage amount suggestion, 
    premium range estimate, and reason for recommendation based on user features.
    """
    age = int(data.get('Age', 30))
    diabetes = data.get('Diabetes', 0)
    heart_disease = data.get('ChronicCond_Heartfailure', 0)
    hospitalization = data.get('HospitalizationHistory', 'No')
    children = int(data.get('Children', 0))
    
    plan_type = "Standard Health Plan"
    coverage_suggestion = "₹3–5 Lakhs"
    premium_range = "₹5,000 - ₹8,000/yr"
    reasons = []

    # Reason gathering
    if risk_score == 'High Risk':
        reasons.append(f"High risk score mapped to {round(risk_prob*100, 1)}% probability.")
    
    if int(diabetes) == 1:
        reasons.append("Diabetes history requires continuous medical coverage.")
        
    if int(heart_disease) == 1:
        reasons.append("Heart disease history requires critical cardiac coverage limits.")
        
    if hospitalization == 'Yes':
        reasons.append("Previous hospitalization indicates potential need for inpatient benefits.")
        
    # Decision Logic
    if risk_score == 'High Risk' or int(diabetes) == 1 or int(heart_disease) == 1:
        plan_type = "Comprehensive Health Plan"
        coverage_suggestion = "₹10–15 Lakhs"
        premium_range = "₹12,000 - ₹20,000/yr"
    elif risk_score == 'Medium Risk':
        plan_type = "Enhanced Health Plan"
        coverage_suggestion = "₹5–10 Lakhs"
        premium_range = "₹8,000 - ₹12,000/yr"

    if children > 0 and plan_type != "Comprehensive Health Plan":
        plan_type = "Family Floater Plan"
        reasons.append(f"Added dependents ({children}) triggered Family plan recommendation.")
        
    if not reasons:
        reasons.append("Low health risk and clean history allow for standard economic coverage.")

    return {
        'recommended_plan': plan_type,
        'coverage_suggestion': coverage_suggestion,
        'premium_range': premium_range,
        'reason': " ".join(reasons)
    }
