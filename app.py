# # -*- coding: utf-8 -*-
# """
# Created on Tue Jun 20 23:48:05 2023

# @author: SUJANA KOLA
# """

from flask import Flask, request, render_template, jsonify, session
import pickle
import numpy as np
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'thyroid_classification_key')

# Load the trained model
model = pickle.load(open('thyroid_model.pkl', 'rb'))

# Feature names and descriptions
FEATURES = {
    'TSH': {'name': 'Thyroid Stimulating Hormone', 'unit': 'mU/L', 'normal_range': '0.4-4.0'},
    'T3': {'name': 'Triiodothyronine', 'unit': 'ng/dL', 'normal_range': '0.6-1.8'},
    'TT4': {'name': 'Total Thyroxine', 'unit': 'μg/dL', 'normal_range': '5.0-12.0'},
    'T4U': {'name': 'T4 Uptake Ratio', 'unit': 'ratio', 'normal_range': '0.75-1.25'},
    'FTI': {'name': 'Free Thyroxine Index', 'unit': 'ratio', 'normal_range': '6.0-12.0'}
}

@app.route('/')
def home():
    return render_template("home.html")

def get_value_status(value, feature):
    """Determine if a value is within normal range"""
    if feature not in FEATURES:
        return "Unknown"
    
    normal_range = FEATURES[feature]['normal_range']
    low, high = map(float, normal_range.split('-'))
    
    if value < low:
        return "Low"
    elif value > high:
        return "High"
    else:
        return "Normal"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get numerical features
        TSH = float(request.form["TSH"])
        T3 = float(request.form["T3"])
        TT4 = float(request.form["TT4"])
        T4U = float(request.form["T4U"])
        FTI = float(request.form["FTI"])
        
        # Get categorical features and convert to binary
        sex_M = 1 if request.form['sex'] == "sex_M" else 0
        sick_t = 1 if request.form['sick'] == "sick_t" else 0
        pregnant_t = 1 if request.form['pregnant'] == "pregnant_t" else 0
        thyroid_surgery_t = 1 if request.form['thyroid_surgery'] == "thyroid_surgery_t" else 0
        goitre_t = 1 if request.form['goitre'] == "goitre_t" else 0
        tumor_t = 1 if request.form['tumor'] == "tumor_t" else 0

        # Create feature array
        features = [[TSH, T3, TT4, T4U, FTI, sex_M, sick_t, pregnant_t, 
                    thyroid_surgery_t, goitre_t, tumor_t]]
        
        # Make prediction
        prediction = model.predict(features)
        output = prediction[0]
        
        # Map prediction to result
        result_map = {
            0: 'HYPERTHYROID',
            1: 'HYPOTHYROID',
            2: 'NEGATIVE',
            3: 'SICK'
        }
        
        # Create explanation
        numerical_values = {
            'TSH': TSH,
            'T3': T3,
            'TT4': TT4,
            'T4U': T4U,
            'FTI': FTI
        }
        
        abnormal_values = []
        for feature, value in numerical_values.items():
            status = get_value_status(value, feature)
            if status != "Normal":
                abnormal_values.append({
                    'feature': feature,
                    'value': value,
                    'status': status,
                    'name': FEATURES[feature]['name'],
                    'unit': FEATURES[feature]['unit'],
                    'normal_range': FEATURES[feature]['normal_range']
                })
        
        risk_factors = []
        if sick_t:
            risk_factors.append("Current illness")
        if thyroid_surgery_t:
            risk_factors.append("Previous thyroid surgery")
        if goitre_t:
            risk_factors.append("Presence of goitre")
        if tumor_t:
            risk_factors.append("Presence of tumor")
        
        explanation = {
            'abnormal_values': abnormal_values,
            'risk_factors': risk_factors,
            'prediction': result_map.get(output, "UNKNOWN")
        }
        
        # Store in session for the explain endpoint
        session['explanation'] = explanation
        
        result = f'Thyroid Classification Result: {result_map.get(output, "UNKNOWN")}'
        return render_template('home.html', y=result, explanation=explanation)
        
    except Exception as e:
        error_message = f'Error: {str(e)}'
        return render_template('home.html', y=error_message)

@app.route('/explain', methods=['GET'])
def explain():
    try:
        explanation = session.get('explanation', {})
        return jsonify(explanation)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
