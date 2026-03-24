from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)
APP_STARTUP_ERROR = None

try:
    from flask_cors import CORS
    from prediction import get_prediction
    from analytics import perform_claim_analytics
    from recommendation_engine import generate_recommendation
    from preventive_care import generate_preventive_care
    
    CORS(app)
except Exception as e:
    APP_STARTUP_ERROR = traceback.format_exc()

if APP_STARTUP_ERROR:
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=['GET', 'POST'])
    def catch_all(path):
        return jsonify({
            'success': False,
            'error': 'Backend Initialization Failed',
            'traceback': APP_STARTUP_ERROR
        }), 500
else:
    @app.route('/')
    def index():
        return jsonify({
            'status': 'online',
            'message': 'Health Prediction API is running. Interaction is handled by the integrated dashboard frontend.',
            'endpoints': {
                '/predict': 'POST only - Send health data to get predictions'
            }
        })
    @app.route('/api/predict', methods=['GET', 'POST'])
    def predict():
        if request.method == 'GET':
            return jsonify({
                'success': False,
                'error': 'Method Not Allowed',
                'message': 'This endpoint requires a POST request with health metric data. Please use the dashboard to submit your data.'
            }), 405
        
        try:
            data = request.json
            
            # 1. Get exact model prediction
            pred_data = get_prediction(data)
            risk_level = pred_data['risk_level']
            risk_probability = pred_data['risk_probability']
            key_factors = pred_data['key_factors']
            
            # 2. Get Claim Risk Analytics
            analytics = perform_claim_analytics(risk_level, risk_probability, data)
            
            # 3. Get Insurance Recommendations
            insurance = generate_recommendation(risk_level, risk_probability, data)
            
            # 4. Get Preventive Care Guidance
            preventive_care = generate_preventive_care(risk_level, data)
            
            return jsonify({
                'success': True,
                'prediction': {
                    'risk_level': risk_level,
                    'risk_probability': risk_probability,
                    'key_factors': key_factors
                },
                'analytics': analytics,
                'insurance': insurance,
                'preventive_care': preventive_care
            })

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
