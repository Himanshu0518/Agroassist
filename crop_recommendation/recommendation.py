from flask import Blueprint, render_template, request, jsonify, url_for
import numpy as np
import pandas as pd
import joblib
import json
import requests
import os
import ee
import matplotlib
matplotlib.use('Agg')  # For headless servers (no GUI)
import matplotlib.pyplot as plt
import datetime
import pandas as pd

recom_bp = Blueprint('recommendation', __name__, template_folder='templates', static_folder='static', url_prefix='/recommendation')

AGRO_API_KEY = os.getenv("AGRO_API_KEY", "c2339a94d63f41b15e4b9f88bc4d2ca6")

# 1) Load Models
crop_recommendation_model = joblib.load("predictive_models/crop_recommendation.joblib")
yield_prediction_model = joblib.load("predictive_models/yeild_prediction.joblib")

# 2) Load Crop Mapping
with open("crop_mapping.json", "r") as file:
    crop_mapping = json.load(file)

# 3) Index Route
@recom_bp.route('/')
def recomm_index():
    return render_template('recommendation.html')

############################
# Weather & Remote Sensing #
############################

def get_weather_data(lat, lon):
    """Fetch weather data using AgroMonitoring (OpenWeather-based) API."""
    try:
        api_url = f"https://api.agromonitoring.com/agro/1.0/weather/forecast?lat={lat}&lon={lon}&appid={AGRO_API_KEY}"
        response = requests.get(api_url)
        data = response.json()
       
        # If data is a list, take the first element
        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        # Extract values safely
        temperature = data.get("main", {}).get("temp", 293.11)
        humidity = data.get("main", {}).get("humidity", 84)
        rainfall = data.get("rain", {}).get("1h", data.get("rain", {}).get("3h", 3))

        return {
            "temperature": round(temperature - 273.15, 2),  # K to °C
            "humidity": humidity,
            "rainfall": rainfall
        }

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return {"temperature": 20, "rainfall": 0, "humidity": 70}

def get_remote_sensing_data(latitude, longitude):
    """Fetch remote sensing data from Google Earth Engine."""
    try:
        ee.Initialize(project='ee-hs7875289')
        point = ee.Geometry.Point(longitude, latitude)

        dataset = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
                    .filterBounds(point) \
                    .filterDate("2023-01-01", "2023-12-31") \
                    .sort("system:time_start") \
                    .first()

        ndvi = dataset.normalizedDifference(["B8", "B4"]).rename("NDVI")
        gndvi = dataset.normalizedDifference(["B8", "B3"]).rename("GNDVI")
        ndwi = dataset.normalizedDifference(["B8", "B11"]).rename("NDWI")
        savi = dataset.expression(
            "((NIR - RED) * (1 + 0.5)) / (NIR + RED + 0.5)",
            {"NIR": dataset.select("B8"), "RED": dataset.select("B4")}
        ).rename("SAVI")

        indices = ndvi.addBands([gndvi, ndwi, savi])
        values = indices.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=10,
            maxPixels=1e9
        )

        return {
            "NDVI": values.get("NDVI").getInfo(),
            "GNDVI": values.get("GNDVI").getInfo(),
            "NDWI": values.get("NDWI").getInfo(),
            "SAVI": values.get("SAVI").getInfo(),
            "soil_moisture": 35.0
        }
    except Exception as e:
        print(f"Error fetching remote sensing data: {e}")
        return {"NDVI": 0.5, "GNDVI": 0.4, "NDWI": 0.3, "SAVI": 0.2, "soil_moisture": 35.0}

##########################
# Price Forecasting Part #
##########################

import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_price_forecast(sarima_model, start_date, forecast_steps,crop):
    """
    Plots historical fitted values and forecasts for crop price.
    Assumes sarima_model has been trained with data from 2010 to 2025.
    
    Parameters:
    - sarima_model: Trained SARIMA model with fittedvalues and get_forecast() method.
    - start_date: String or datetime representing the start date for forecasting.
    - forecast_steps: Number of steps (months) to forecast.
    
    Returns:
    - avg_price: Average forecasted price over forecast_steps.
    - plot_path: Path to the saved forecast plot.
    """
    # Convert start_date to datetime if needed
    start_date = pd.to_datetime(start_date)
    
    # Get fitted values (historical predictions)
    fitted_values = sarima_model.fittedvalues
    
    # Forecast the next forecast_steps periods
    forecast_result = sarima_model.get_forecast(steps=forecast_steps)
    forecasted_mean = forecast_result.predicted_mean
    forecast_conf = forecast_result.conf_int()

    # Create a datetime index for historical data (assume monthly frequency)
    fitted_dates = pd.date_range(start="2010-01-01", periods=len(fitted_values), freq="MS")
    fitted_series = pd.Series(fitted_values.values, index=fitted_dates)
    
    # Create datetime index for forecasts
    last_date = fitted_dates[-1]
    forecast_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_steps, freq="MS")
    forecast_series = pd.Series(forecasted_mean.values, index=forecast_dates)
    
    # Ensure the forecast confidence interval index matches forecast dates
    forecast_conf.index = forecast_dates
    
    # Plot historical fitted values and forecasts
    plt.figure(figsize=(10, 6))
    plt.plot(fitted_series, label="Historical Fitted Values", color="blue")
    plt.plot(forecast_series, label="Forecast", color="red")
    plt.fill_between(forecast_dates, 
                     forecast_conf.iloc[:, 0], 
                     forecast_conf.iloc[:, 1], color="pink", alpha=0.3, label="Confidence Interval")
    
    plt.xlabel("Date")
    plt.ylabel("Price (₹)")
    plt.title("Crop Price Forecast and Historical Fitted Values")
    plt.legend()
    
    # Ensure the static/forecast_plots directory exists
    plot_dir = os.path.join("static", "forecast_plots")
    os.makedirs(plot_dir, exist_ok=True)
    
    # Save plot
    plot_path = os.path.join(plot_dir, f"{crop}_price_forecast.png")
    plt.savefig(plot_path, dpi=100, bbox_inches="tight")
    plt.close()
    
    # Calculate average forecasted price
    avg_price = forecast_series.mean()
    return avg_price, plot_path


import os
import joblib

def forecast_price_sarima(crop_name, start_date_str):
    """
    Forecasts crop price using a trained SARIMA model.
    
    Parameters:
    - crop_name: Name of the crop (string).
    - start_date_str: Start date for forecasting (string format).

    Returns:
    - avg_price: Predicted average price for the next 4 months.
    - plot_path: Path to the saved forecast plot (if successful), else None.
    """
    try:
        model_path = f"predictive_models/{crop_name}_price_prediction.joblib"
        
        # Check if model file exists
        if not os.path.exists(model_path):
            print(f"No price model found for {crop_name}, using default price = ₹50,000")
            return 50000, None
        
        # Load SARIMA model
        sarima_model = joblib.load(model_path)
        if sarima_model is None:
            raise ValueError("Loaded model is None, possibly corrupted.")
        
        # Forecast price
        avg_price, plot_path = plot_price_forecast(sarima_model, start_date_str, 8,crop_name)
        return avg_price, plot_path
    
    except FileNotFoundError:
        print(f"Error: Model file for {crop_name} not found.")
    except ValueError as ve:
        print(f"Model error for {crop_name}: {ve}")
    except Exception as e:
        print(f"Unexpected error forecasting price for {crop_name}: {e}")
    
    # Default return in case of any error
    return 50000, None


##########################
# Final Recommendation   #
##########################

@recom_bp.route('/final-recommendation', methods=['POST'])
def final_recommendation():
    try:
        # Basic inputs
        N = float(request.form.get('N'))
        P = float(request.form.get('P'))
        K = float(request.form.get('K'))
        pH = float(request.form.get('pH'))
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))

        # If you have a date input for price forecast
        start_date_str = request.form.get('start_date', "")

        # Get weather & remote sensing data
        weather = get_weather_data(latitude, longitude)
        remote = get_remote_sensing_data(latitude, longitude)

        temperature, rainfall, humidity = weather.values()
        NDVI, GNDVI, NDWI, SAVI, soil_moisture = remote.values()

        recommended_crops = []

        # Crop Recommendation
        feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'Ph', 'rainfall']
        for i in range(6):
            # Variation
            rec_input = pd.DataFrame([[
                N + np.random.uniform(-5, 5),
                P + np.random.uniform(-5, 5),
                K + np.random.uniform(-5, 5),
                temperature + np.random.uniform(-8, 8),
                humidity + np.random.uniform(-5, 5),
                pH + np.random.uniform(-0.5, 0.5),
                rainfall + np.random.uniform(-5, 5)
            ]], columns=feature_names)

            probabilities = crop_recommendation_model.predict_proba(rec_input)[0]
            top_indices = np.argsort(probabilities)[-2:]  # top 2 crops

            for index in reversed(top_indices):
                crop_label = str(index)
                crop_name = crop_mapping.get(crop_label, "Unknown Crop")
                if crop_name not in recommended_crops:
                    recommended_crops.append(crop_name)

        # Build results
        results = []
        for crop in recommended_crops:
            crop_name = crop.capitalize()

            # Yield Prediction
            yield_feature_names = [
                'latitude', 'longitude', 'NDVI', 'GNDVI', 'NDWI', 'SAVI',
                'soil_moisture', 'temperature', 'rainfall', 'crop_type'
            ]
            yield_input = pd.DataFrame([[
                latitude, longitude, NDVI, GNDVI, NDWI, SAVI,
                soil_moisture, temperature, rainfall, crop_name
            ]], columns=yield_feature_names)

            predicted_yield = yield_prediction_model.predict(yield_input)[0]

            # Price Forecasting
            avg_price, forecast_plot = forecast_price_sarima(crop, start_date_str)

            # Production Cost
            production_cost = get_production_cost(crop_name)
            net_profit = (avg_price * predicted_yield) - production_cost
            profitability_score = round((net_profit / production_cost), 2) if production_cost else 0

            results.append({
                "crop": crop_name,
                "predicted_price": round(avg_price, 2),
                "expected_yield": round(predicted_yield, 2),
                "net_profit": round(net_profit, 2),
                "profitability_score": profitability_score,
                "forecast_plot": forecast_plot  # path to the forecast plot
            })
       
        results.sort(key=lambda x: x["profitability_score"], reverse=True)
        
        return render_template("recommendation.html", recommendations=results  )

    except Exception as e:
        return jsonify({"error": str(e)})

def get_production_cost(crop, state="Unknown"):
    with open("production_costs.json", "r") as file:
        cost_data = json.load(file)
    return cost_data.get(crop, {}).get(state, 50000)
