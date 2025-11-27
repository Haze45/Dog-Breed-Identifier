import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'your_model_transfer.h5')
LABELS_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'labels.json')

try:
    # custom_objects = {'relu6': tf.nn.relu6}
    model = tf.keras.models.load_model(MODEL_PATH)
except (IOError, ImportError) as e:
    print(f"Error loading model: {e}")
    print("Please ensure 'your_model.h5' is in the 'backend/app/models/' directory.")
    model = None

try:
    with open(LABELS_PATH, 'r') as f:
        labels = json.load(f)
except FileNotFoundError:
    print(f"Error: '{LABELS_PATH}' not found.")
    print("Please ensure 'labels.json' is in the 'backend/app/models/' directory.")
    labels = None

def preprocess_image(image: Image.Image) -> np.ndarray:
    target_size = (224, 224)
    if image.mode != "RGB":
        image = image.convert("RGB")
        
    image = image.resize(target_size)
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    # image_array = np.expand_dims(image_array, axis=0) / 255.0
    processed_array = tf.keras.applications.mobilenet_v2.preprocess_input(
        np.expand_dims(image_array, axis=0)
    )
    
    return processed_array

def predict_dog_breed(image: Image.Image) -> str:
    if model is None or labels is None:
        return "Model or labels not loaded. Please check server configuration."

    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)
    predicted_index = np.argmax(predictions[0])
    raw_predicted_breed = labels.get(str(predicted_index), "Unknown Breed")

    if '-' in raw_predicted_breed:
        clean_name = raw_predicted_breed.split('-', 1)[1]
    else:
        clean_name = raw_predicted_breed

    final_breed_name = clean_name.replace('_', ' ').title()
    
    return final_breed_name
