#!/usr/bin/env python3
"""
Test script to validate model loading and identify any issues.
Run this script to check if your trained model can be loaded correctly.
"""

import os
import sys
from pathlib import Path

def test_model_loading():
    """Test if the trained model can be loaded correctly."""
    print("Testing model loading...")
    print("=" * 50)
    
    # Check if model directory exists
    model_path = Path("models/autogluon_model")
    if not model_path.exists():
        print("ERROR: Model directory not found at models/autogluon_model")
        print("Please train the model first using: python run_pipeline.py")
        return False
    
    # Check required files
    required_files = ['df_preprocessor.pkl', 'config.yaml', 'model.ckpt']
    missing_files = []
    
    for file in required_files:
        file_path = model_path / file
        if not file_path.exists():
            missing_files.append(file)
        else:
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"SUCCESS: {file} found ({size_mb:.1f} MB)")
    
    if missing_files:
        print(f"ERROR: Missing required files: {missing_files}")
        return False
    
    # Try importing AutoGluon
    try:
        from autogluon.multimodal import MultiModalPredictor
        print("SUCCESS: AutoGluon imported successfully")
    except ImportError as e:
        print(f"ERROR: Failed to import AutoGluon: {e}")
        print("Please install AutoGluon: pip install autogluon.multimodal")
        return False
    
    # Try loading the model
    try:
        print("\nAttempting to load model...")
        predictor = MultiModalPredictor.load(str(model_path))
        print("SUCCESS: Model loaded successfully!")
        
        # Check model attributes
        if hasattr(predictor, 'class_labels'):
            print(f"Number of classes: {len(predictor.class_labels)}")
            print(f"Class labels: {predictor.class_labels}")
        else:
            print("WARNING: No class labels found")
        
        # Test a simple prediction
        print("\nTesting prediction...")
        import pandas as pd
        import tempfile
        from PIL import Image
        
        # Create a dummy image for testing
        dummy_image = Image.new('RGB', (224, 224), color='red')
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            dummy_image.save(tmp.name)
            test_df = pd.DataFrame({'image': [tmp.name], 'label': [0]})
        
        try:
            prediction = predictor.predict(test_df)
            print(f"SUCCESS: Prediction test passed. Predicted: {prediction[0]}")
            os.unlink(tmp.name)
        except Exception as e:
            print(f"WARNING: Prediction test failed: {e}")
            if os.path.exists(tmp.name):
                os.unlink(tmp.name)
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to load model: {e}")
        
        # Provide specific guidance based on error type
        error_msg = str(e)
        if "Missing key(s) in state_dict" in error_msg or "size mismatch" in error_msg:
            print("\nThis appears to be an architecture mismatch error.")
            print("Possible solutions:")
            print("1. Retrain the model using the current configuration")
            print("2. Check if the model was trained with different hyperparameters")
            print("3. Ensure the training and loading environments are consistent")
        elif "CUDA" in error_msg:
            print("\nThis appears to be a GPU/CUDA error.")
            print("Possible solutions:")
            print("1. Try running on CPU only")
            print("2. Check CUDA installation and compatibility")
            print("3. Set CUDA_VISIBLE_DEVICES='' to force CPU usage")
        
        return False

def main():
    """Main function to run the test."""
    print("Pet Breed Classifier - Model Loading Test")
    print("=" * 50)
    
    success = test_model_loading()
    
    print("\n" + "=" * 50)
    if success:
        print("SUCCESS: Model loading test passed!")
        print("Your model should work correctly with the Streamlit app.")
    else:
        print("ERROR: Model loading test failed!")
        print("Please fix the issues above before running the Streamlit app.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 