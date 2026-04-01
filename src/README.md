# src/ Directory

This directory contains **Machine Learning development files** that are NOT part of the Django application.

## ⚠️ Important Note

These files are kept for **model training and development purposes only**. They are:
- ❌ NOT imported by Django
- ❌ NOT used in production
- ✅ Used only for ML model training/evaluation
- ✅ Documented for future model updates

## 📂 Files

### Training Scripts
- **train.py** - CNN model training for rice disease detection
  - Uses MobileNetV2 architecture
  - Creates `models/rice_disease_model.h5`
  - Generates training history and metrics
  
- **yield_train.py** - Yield prediction model training
  - Uses regression model
  - Creates `models/yield_model.joblib`
  - Trains on `dataset/yield_sample_new.csv`

### Evaluation
- **evaluate.py** - Model evaluation script
  - Tests model accuracy
  - Generates confusion matrix
  - Creates ROC curves
  
- **evaluate.ipynb** - Jupyter notebook for interactive evaluation
  - Visual analysis of model performance
  - Plots and metrics

### Flask Demo (Legacy)
- **app_flask.py** - Standalone Flask API demo
  - ⚠️ Not used in Django production
  - Kept for reference/testing
  - Demonstrates ML model inference

### Conversion
- **convert_tflite.py** - Convert H5 model to TensorFlow Lite
  - For mobile deployment
  - Creates `models/agriscan.tflite`

## 🚫 Why Not Delete?

These files are kept because:
1. **Model Retraining** - Needed when updating the disease detection model
2. **Documentation** - Shows how models were created
3. **Reproducibility** - Can reproduce model training
4. **Reference** - Future developers can understand ML pipeline

## 🔧 Usage

### Training New Model
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Train disease detection model
python src/train.py

# Train yield prediction model
python src/yield_train.py

# Evaluate model
python src/evaluate.py
```

### Converting to TFLite
```bash
python src/convert_tflite.py
```

## 📊 Model Files Generated

After training, these files are created in `models/`:
- `rice_disease_model.h5` - Disease detection CNN
- `yield_model.joblib` - Yield prediction model
- `class_names.json` - Disease class mappings
- `rice_disease_model_history.json` - Training metrics
- `agriscan.tflite` - Mobile-optimized model

## 🔗 Django Integration

The Django app (`polls/views.py`) loads the trained models:
```python
# In Django views
model = tf.keras.models.load_model('models/rice_disease_model.h5')
yield_model = joblib.load('models/yield_model.joblib')
```

**The training scripts are NOT imported by Django.**

## 🗂️ Dataset Structure

Expected structure for training:
```
dataset/
├── train/              # Training data (70%)
│   ├── bacterial_leaf_blight/
│   ├── brown_spot/
│   ├── healthy/
│   ├── leaf_blast/
│   └── ...
├── test/               # Test data (held-out)
│   └── (same structure)
├── validation/         # Validation data (30%)
│   └── (same structure)
└── yield_sample_new.csv  # Yield training data
```

## 📝 Best Practice

### DO ✅
- Keep these files for model maintenance
- Document model training process
- Version control training scripts
- Exclude large datasets from git

### DON'T ❌
- Import these files in Django
- Run training on production server
- Commit trained model files (too large)
- Delete without backup

## 🔄 Model Update Process

1. Collect new training data
2. Update `dataset/` directory
3. Run `python src/train.py`
4. Evaluate with `python src/evaluate.py`
5. If satisfied, replace model in `models/`
6. Test in Django app
7. Deploy updated model

---

**Purpose**: ML development and model training  
**Used in Django**: ❌ No  
**Delete?**: ❌ No - Keep for model maintenance  
**Last Updated**: 2026-02-22
