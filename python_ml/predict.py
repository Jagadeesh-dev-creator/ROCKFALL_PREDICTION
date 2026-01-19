"""
Flask API for Rockfall Risk Prediction
Endpoint: POST /predict
Input: {slope, rainfall, temperature}
Output: {risk_level, probability, message}
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load trained model + metadata
MODEL_PATH = 'models/rockfall_model.pkl'
META_PATH = Path(__file__).resolve().parents[0] / 'models' / 'feature_metadata.pkl'
model = None
feature_means = None
feature_columns = None

def load_model():
    """Load the trained model"""
    global model, feature_means, feature_columns
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully")
    else:
        print("❌ Model not found. Please run train.py first.")
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

    if META_PATH.exists():
        meta = joblib.load(META_PATH)
        feature_means = meta.get("feature_means", {})
        feature_columns = meta.get("feature_columns", [])
        print(f"✅ Feature metadata loaded: {len(feature_columns)} columns")
    else:
        raise FileNotFoundError(f"Feature metadata not found at {META_PATH}")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "feature_columns": feature_columns,
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict rockfall risk
    Expected JSON: {"slope": float, "rainfall": float, "temperature": float}
    Internally pads missing features with training-set means to match the
    15-feature model.
    """
    try:
        # Parse input
        data = request.get_json()
        
        # Validate input
        required_fields = ['slope', 'rainfall', 'temperature']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        # Extract features
        slope = float(data['slope'])
        rainfall = float(data['rainfall'])
        temperature = float(data['temperature'])
        
        # Validate ranges
        if not (0 <= slope <= 90):
            return jsonify({"error": "Slope must be between 0-90 degrees"}), 400
        if not (0 <= rainfall <= 500):
            return jsonify({"error": "Rainfall must be between 0-500 mm"}), 400
        if not (-50 <= temperature <= 60):
            return jsonify({"error": "Temperature must be between -50 to 60°C"}), 400
        
        # Prepare full feature vector using training means as defaults
        if feature_means is None or feature_columns is None:
            return jsonify({"error": "Model metadata not loaded."}), 500

        feature_values = dict(feature_means)
        feature_values['slope_angle_deg'] = slope
        feature_values['temperature_c'] = temperature
        feature_values['rain_flag'] = 1 if rainfall > 0 else 0

        # Build ordered vector
        try:
            vector = [feature_values[col] for col in feature_columns]
        except KeyError as missing:
            return jsonify({"error": f"Missing feature in metadata: {missing}"}), 500

        features = np.array([vector], dtype=float)
        
        # Make prediction
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        # Map risk levels
        risk_labels = ['Low', 'Medium', 'High']
        risk_level = risk_labels[prediction]
        confidence = float(probabilities[prediction]) * 100
        
        # Generate message
        messages = {
            'Low': '✅ Rockfall risk is LOW. Conditions are stable.',
            'Medium': '⚠️ Rockfall risk is MEDIUM. Exercise caution.',
            'High': '🚨 Rockfall risk is HIGH! Evacuate immediately!'
        }
        
        response = {
            "risk_level": risk_level,
            "risk_code": int(prediction),
            "confidence": round(confidence, 2),
            "probabilities": {
                "low": round(float(probabilities[0]) * 100, 2),
                "medium": round(float(probabilities[1]) * 100, 2),
                "high": round(float(probabilities[2]) * 100, 2)
            },
            "message": messages[risk_level],
            "input": {
                "slope": slope,
                "rainfall": rainfall,
                "temperature": temperature
            }
        }
        
        return jsonify(response)
    
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    # Load model on startup
    load_model()
    
    # Run Flask app
    print("🚀 Starting Flask API on http://localhost:5000")
    print("📡 Endpoint: POST /predict")
    app.run(host='0.0.0.0', port=5000, debug=True)
