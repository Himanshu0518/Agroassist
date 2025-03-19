from flask import Blueprint, render_template , session , redirect , url_for,request,flash,current_app , jsonify
import sqlite3
from werkzeug.utils import secure_filename
import os
from datetime import datetime 
import numpy as np 
import pandas as pd
import joblib
#import json

recom_bp = Blueprint('recommendation', __name__, template_folder='templates', static_folder='static', url_prefix='/recommendation')



# Load models
crop_recommendation_model = joblib.load('crop_recommendation.joblib')
price_prediction_model = joblib.load('price_prediction.pkl')


@recom_bp.route('/recommend-crops', methods=['POST'])
def recommend_crops():
    data = request.get_json()
    soil_type = data['soil_type']
    rainfall = data['rainfall']
    temperature = data['temperature']
    
    # Predict recommended crops
    input_data = np.array([[soil_type, rainfall, temperature]])
    recommended_crops = crop_recommendation_model.predict(input_data)
    
    return jsonify({'recommended_crops': recommended_crops.tolist()})

@recom_bp.route('/predict-price', methods=['POST'])
def predict_price():
    data = request.get_json()
    crop = data['crop']
    
    # Predict price
    predicted_price = price_prediction_model.predict([[crop]])
    
    return jsonify({'crop': crop, 'predicted_price': predicted_price[0]})

@recom_bp.route('/final-recommendation', methods=['POST'])
def final_recommendation():
    data = request.get_json()
    soil_type = data['soil_type']
    rainfall = data['rainfall']
    temperature = data['temperature']
    
    # Step 1: Get recommended crops
    input_data = np.array([[soil_type, rainfall, temperature]])
    recommended_crops = crop_recommendation_model.predict(input_data)

    # Step 2: Predict price and calculate profitability
    results = []
    for crop in recommended_crops:
        predicted_price = price_prediction_model.predict([[crop]])[0]
        expected_yield = get_expected_yield(crop)  # Custom function
        production_cost = get_production_cost(crop)  # Custom function
        
        profitability = (predicted_price * expected_yield - production_cost) / production_cost
        
        results.append({
            'crop': crop,
            'predicted_price': predicted_price,
            'profitability_score': profitability
        })

    # Rank by profitability
    results = sorted(results, key=lambda x: x['profitability_score'], reverse=True)
    
    return jsonify({'final_recommendations': results})

def get_expected_yield(crop):
    # Example: Load from dataset or use a dictionary
    yield_data = {'wheat': 1.5, 'rice': 2.0, 'maize': 1.2}
    return yield_data.get(crop, 1.0)

def get_production_cost(crop):
    # Example: Load from dataset or use a dictionary
    cost_data = {'wheat': 500, 'rice': 600, 'maize': 400}
    return cost_data.get(crop, 500)


