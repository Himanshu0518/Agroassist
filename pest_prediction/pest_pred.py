from flask import Flask, Blueprint, render_template, request, jsonify
import requests
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Create a Blueprint for pest detection
pest_bp = Blueprint(
    'pest_prediction', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    url_prefix='/pest_prediction'
)
CROP_PEST_API_KEY = 'sk-ZQ0167ed9a9b486c69571'

model = tf.keras.models.load_model('predictive_models/pest_prediction.h5')

# Define the target image size expected by your model (e.g., 224x224)
IMG_HEIGHT, IMG_WIDTH = 150, 150

def get_hardiness_zone(species_name):

    url = f"https://perenual.com/api/hardiness-map?species_id={species_name}&key={CROP_PEST_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch data"}


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
        
        image = Image.open(io.BytesIO(image_file.read()))
        image = image.convert("RGB")  # Ensure image is in RGB format

        # Resize image to the size expected by your model
        image = image.resize((IMG_WIDTH, IMG_HEIGHT))
        image_array = np.array(image)

        # Normalize the image array if needed (e.g., scale pixel values to [0, 1])
        image_array = image_array.astype("float32") / 255.0

        # Expand dimensions to match the model input shape (batch_size, height, width, channels)
        image_array = np.expand_dims(image_array, axis=0)

        # Make predictions using the CNN model
        predictions = model.predict(image_array)

        # Process the prediction result as needed. For example:
        # If using softmax output, get the index of the highest score:
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = np.max(predictions, axis=1)[0]

        # Debug output
        print("Predicted Class:", predicted_class)
        print("Confidence:", confidence)
        hardiness_info = get_hardiness_zone(crop_name)
        print( hardiness_info)
        # Pass results to frontend
        return render_template("pest.html", pest_result=crop_lst[predicted_class-1], crop_name=crop_name, hardiness=hardiness_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500 