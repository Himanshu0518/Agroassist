from flask import Blueprint, render_template, request, jsonify, url_for
import tensorflow as tf 
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

pest_bp = Blueprint('pest_prediction', __name__, template_folder='templates', static_folder='static', url_prefix='/pest_prediction')

# est_model = tf.keras.models.load_model('my_model') 

@pest_bp.route('/')
def pest_index():
    return render_template('pest.html')