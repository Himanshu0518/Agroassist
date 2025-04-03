from flask import Blueprint, render_template, request, jsonify
import requests
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os 

# Create a Blueprint for pest detection
pest_bp = Blueprint(
    'pest_prediction', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    url_prefix='/pest_prediction'
)
CROP_PEST_API_KEY = os.getenv('CROP_PEST_API_KEY')
interpreter = tf.lite.Interpreter(model_path="predictive_models/pest_prediction.tflite")
interpreter.allocate_tensors()

# Get input & output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define the target image size expected by your model
IMG_HEIGHT, IMG_WIDTH = 150, 150

def get_hardiness_map(species_id):
    url = f"https://perenual.com/api/hardiness-map?species_id={species_id}&key={CROP_PEST_API_KEY}"
    response = requests.get(url)
    return url if response.status_code == 200 else None

@pest_bp.route('/pest_detection')
def pest_index():
    return render_template('pest.html')

@pest_bp.route('/image_classification', methods=['POST'])
def image_classification():
    if 'pest_img' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['pest_img']
    crop_name = request.form.get('pest_crop_name')

    try:
        crop_lst = ['Apple_scab', 'Black_rot', 'Cedar_apple_rust', 'healthy', 'healthy', 
                    'Powdery_mildew', 'healthy', 'Cercospora_leaf_spot Gray_leaf_spot', 'Common_rust_', 'Northern_Leaf_Blight', 
                    'healthy', 'Black_rot', 'Esca_(Black_Measles)', 'Leaf_blight_(Isariopsis_Leaf_Spot)', 'healthy', 
                    'Haunglongbing_(Citrus_greening)', 'Bacterial_spot', 'healthy', 'Bacterial_spot', 'healthy', 'Early_blight',
                    'Late_blight', 'healthy', 'healthy', 'healthy', 'Powdery_mildew', 'Leaf_scorch', 'healthy', 'Bacterial_spot',
                    'Early_blight', 'Late_blight', 'Leaf_Mold', 'Septoria_leaf_spot', 'Spider_mites Two-spotted_spider_mite', 
                    'Target_Spot', 'Tomato_Yellow_Leaf_Curl_Virus', 'Tomato_mosaic_virus', 'healthy']
        
        # Process the uploaded image
        image = Image.open(io.BytesIO(image_file.read()))
        image = image.convert("RGB")  # Ensure image is in RGB format
        image = image.resize((IMG_WIDTH, IMG_HEIGHT))
        image_array = np.array(image, dtype=np.float32) / 255.0  # Normalize pixels
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

        # Run inference using TFLite model
        interpreter.set_tensor(input_details[0]['index'], image_array)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])

        # Get the predicted class
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Fetch species details
        species_url = f"https://perenual.com/api/species-list?key={CROP_PEST_API_KEY}&q={crop_name}"
        species_response = requests.get(species_url).json()
        
        hardiness_url = None
        if "data" in species_response and species_response["data"]:
            species_id = species_response["data"][0]["id"]
            hardiness_url = get_hardiness_map(species_id)
            print(f"Species ID: {species_id}")
            print(f"Hardiness Map: {hardiness_url}")

        return render_template("pest.html", 
                               pest_result=crop_lst[predicted_class-1], 
                               crop_name=crop_name, 
                               hardiness_map=hardiness_url)

    except Exception as e:
        return jsonify({"error": str(e)}), 500