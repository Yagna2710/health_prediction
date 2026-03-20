def perform_claim_analytics(risk_level, risk_prob, data):
    """
    Analyzes historical data inputs to output claim frequency, 
    average claim cost, fraud patterns, and future claim probability.
    """
    history = data.get('ClaimHistory_Frequency', '0')
    hosp = data.get('HospitalizationHistory', 'No')
    
    # Base estimations
    avg_claim_cost = 0
    freq_desc = "Low"
    fraud_pattern = "None Detected"
    
    if history == '0':
        freq_desc = "Low (-0 Avg/yr)"
        avg_claim_cost = 0
    elif history == '1-2':
        freq_desc = "Medium (~1 Avg/yr)"
        avg_claim_cost = 45000
    else:
        freq_desc = "High (3+ Avg/yr)"
        avg_claim_cost = 125000
        
    if hosp == 'Yes' and history == '0':
         fraud_pattern = "Abnormal: Hospitalized but 0 claims"
         
    # Estimated Future Cost based on continuous risk probability and age
    age = int(data.get('Age', 30))
    base_cost = 15000 + (age * 100)
    future_claim_prob = min(0.95, risk_prob * 1.2)
    
    estimated_future_cost = base_cost * (1.0 + future_claim_prob)
    
    if hosp == 'Yes':
        estimated_future_cost *= 2.0
        
    return {
        'claim_frequency': freq_desc,
        'average_claim': round(avg_claim_cost),
        'fraud_or_abnormal_patterns': fraud_pattern,
        'future_claim_probability': round(future_claim_prob, 2),
        'estimated_cost': round(estimated_future_cost)
    }
