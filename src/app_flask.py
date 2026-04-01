"""Flask app for AgriScan demo.

Serves multi-page static HTML from web_demo and exposes:
- /predict (image → multi-class disease classification)
- /yield/predict (JSON → rice yield regression)
"""

import os
import io
import json
import re
from typing import Dict, List

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from PIL import Image
import tensorflow as tf

# Compute project root relative to this file to avoid hard-coded paths
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(THIS_DIR)

MODEL_PATH = os.path.join(BASE_DIR, 'models', 'rice_disease_model.h5')
CLASS_MAP_PATH = os.path.join(BASE_DIR, 'models', 'class_names.json')
YIELD_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'yield_model.joblib')

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'web_demo'),
    template_folder=os.path.join(BASE_DIR, 'web_demo'),
    static_url_path=''  # serve static at root (/styles.css, /app.js)
)

# Load models once at startup
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Missing trained model at {MODEL_PATH}. Run src/train.py first.")
model = tf.keras.models.load_model(MODEL_PATH)
if not os.path.exists(CLASS_MAP_PATH):
    raise FileNotFoundError(f"Missing class map at {CLASS_MAP_PATH}. Train the model to generate it.")

with open(CLASS_MAP_PATH, 'r', encoding='utf-8') as fp:
    class_map = json.load(fp)
if isinstance(class_map, dict) and 'labels' in class_map:
    CLASS_NAMES: List[str] = class_map['labels']
elif isinstance(class_map, list):
    CLASS_NAMES = class_map
else:
    CLASS_NAMES = [label for _, label in sorted((int(k), v) for k, v in class_map.items())]

try:
    yield_model = joblib.load(YIELD_MODEL_PATH)
except Exception as e:
    yield_model = None
    print(f"[WARN] Yield model not loaded: {e}")
IMG_SIZE = (224, 224)
TOP_K = 3

def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _pretty_label(value: str) -> str:
    return re.sub(r"[_]+", " ", value).replace("-", " ").title()


DISEASE_INFO: Dict[str, Dict[str, str]] = {
    "bacterial_leaf_blight": {
        "description": "Bacterial infection causing water-soaked lesions along leaf margins.",
        "treatment": "Use resistant varieties and apply copper-based bactericides as needed.",
    },
    "brown_spot": {
        "description": "Fungal spores create brown circular lesions with yellow halos.",
        "treatment": "Improve soil fertility and apply triazole fungicides if severe.",
    },
    "leaf_blast": {
        "description": "Diamond lesions with gray centers caused by Magnaporthe oryzae.",
        "treatment": "Apply systemic fungicide at booting and maintain balanced nitrogen.",
    },
    "leaf_scald": {
        "description": "Large wavy lesions that look scalded due to fungal pathogens.",
        "treatment": "Ensure good drainage and rotate fields to reduce inoculum.",
    },
    "narrow_brown_spot": {
        "description": "Long narrow lesions mainly on leaves and panicles.",
        "treatment": "Apply benzimidazole fungicide when lesions expand quickly.",
    },
    "neck_blast": {
        "description": "Neck region darkens causing panicle breakage.",
        "treatment": "Spray targeted fungicides at heading stage.",
    },
    "rice_hispa": {
        "description": "Insect feeding leaves whitish streaks and transparent patches.",
        "treatment": "Use light traps and apply recommended insecticides if outbreak occurs.",
    },
    "sheath_blight": {
        "description": "Oval green-gray lesions on sheath spread rapidly in humid fields.",
        "treatment": "Improve spacing and spray validamycin or propiconazole.",
    },
    "tungro": {
        "description": "Leafhoppers transmit virus leading to orange-yellow leaves.",
        "treatment": "Plant resistant varieties and control vector population early.",
    },
    "healthy": {
        "description": "No visible disease symptoms detected.",
        "treatment": "Continue monitoring and maintain good field hygiene.",
    },
}


def prepare_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


@app.route('/')
def index():
    # Redirect root to a simple landing page (scan is the primary flow)
    return render_template('login.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/scan')
def scan_page():
    return render_template('scan.html')


@app.route('/prediction')
def prediction_page():
    return render_template('prediction.html')


@app.route('/profile')
def profile_page():
    return render_template('profile.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded.'}), 400
    file = request.files['image']
    img_bytes = file.read()
    x = prepare_image(img_bytes)
    preds = model.predict(x)[0]
    top_indices = np.argsort(preds)[-TOP_K:][::-1]
    best_idx = int(top_indices[0])
    raw_label = CLASS_NAMES[best_idx]
    label = _pretty_label(raw_label)
    confidence = float(preds[best_idx])
    top_predictions = [
        {
            'label': _pretty_label(CLASS_NAMES[int(idx)]),
            'confidence': float(preds[int(idx)]),
            'confidence_pct': float(preds[int(idx)] * 100),
            'info': DISEASE_INFO.get(_slugify(CLASS_NAMES[int(idx)]), {}),
        }
        for idx in top_indices
    ]
    payload = {
        'label': label,
        'confidence': confidence,
        'confidence_pct': confidence * 100,
        'top_predictions': top_predictions,
        'info': DISEASE_INFO.get(_slugify(raw_label), {}),
    }
    return jsonify(payload)


@app.route('/yield/predict', methods=['POST'])
def yield_predict():
    """Predict yield based on structured inputs.

    Expected JSON body:
    {
      "variety": "Rc222",
      "field_area_ha": 1.5,
      "health": "healthy|diseased|...",
      "planting_date": "2025-06-15",
      "growth_duration_days": 110
    }
    Returns per-hectare prediction and total sacks.
    """
    if yield_model is None:
        return jsonify({'error': 'Yield model not available. Train first.'}), 503

    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid JSON'}), 400

    required = ['variety', 'field_area_ha', 'health', 'planting_date', 'growth_duration_days']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    # Convert planting_date to month (pipeline expects planting_month)
    try:
        planting_month = int(pd.to_datetime(data['planting_date']).month)
    except Exception:
        return jsonify({'error': 'Invalid planting_date'}), 400

    # Normalize health to numeric like the training script
    def _parse_health(v):
        if v is None:
            return 0.0
        s = str(v).strip().lower()
        if s in {"healthy", "none", "good"}:
            return 0.0
        if s in {"diseased", "sick", "bad"}:
            return 1.0
        try:
            return float(s)
        except Exception:
            return 0.0

    row = {
        'variety': str(data['variety']).strip(),
        'field_area_ha': float(data['field_area_ha']),
        'health': float(_parse_health(data['health'])),
        'planting_month': planting_month,
        'growth_duration_days': int(data['growth_duration_days'])
    }

    df = pd.DataFrame([row])
    try:
        per_ha = float(yield_model.predict(df)[0])
    except Exception as e:
        return jsonify({'error': f'Prediction error: {e}'}), 500

    total = per_ha * row['field_area_ha']
    return jsonify({
        'predicted_yield_sacks_per_ha': per_ha,
        'field_area_ha': row['field_area_ha'],
        'total_sacks': float(total)
    })


if __name__ == '__main__':
    # Bind to localhost; adjust port as needed
    app.run(debug=True, host='0.0.0.0', port=7000)
