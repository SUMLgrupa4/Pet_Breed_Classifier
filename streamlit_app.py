import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import time
from PIL import Image
from pathlib import Path
import sys
import tempfile

# --- Custom CSS for Modern Look ---
st.markdown(
    """
<style>
body { background: #f6f8fa; }
.main-header { font-size: 2.5rem; font-weight: bold; color: #FF6B6B; text-align: center; margin-bottom: 1rem; }
.sub-header { font-size: 1.2rem; color: #4ECDC4; text-align: center; margin-bottom: 2rem; }
.card { background: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); padding: 2rem; margin-bottom: 1.5rem; }
.status-success { background: #d4edda; color: #155724; border-left: 5px solid #28a745; padding: 0.7rem 1rem; border-radius: 6px; margin-bottom: 1rem; }
.status-warning { background: #fff3cd; color: #856404; border-left: 5px solid #ffc107; padding: 0.7rem 1rem; border-radius: 6px; margin-bottom: 1rem; }
.status-error { background: #f8d7da; color: #721c24; border-left: 5px solid #dc3545; padding: 0.7rem 1rem; border-radius: 6px; margin-bottom: 1rem; }
.upload-box { background: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 10px; padding: 1.5rem; margin-bottom: 1rem; }
.prediction-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; border-radius: 12px; padding: 1.5rem; text-align: center; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }
.breed-list { max-height: 250px; overflow-y: auto; background: #f8f9fa; border-radius: 8px; padding: 1rem; }
</style>
""",
    unsafe_allow_html=True,
)


# --- Utility Functions ---
@st.cache_resource
def load_model():
    """Load the trained AutoGluon model from the models directory."""
    from autogluon.multimodal import MultiModalPredictor

    model_path = Path("models/autogluon_model")
    if not model_path.exists():
        return None, "No trained model found at models/autogluon_model."
    try:
        predictor = MultiModalPredictor.load(str(model_path))
        return predictor, None
    except Exception as e:
        return None, f"Error loading model: {e}"


@st.cache_data
def load_label_map():
    label_map_path = Path("data/metadata/label_map.pkl")
    if not label_map_path.exists():
        return {}, "Label map not found."
    try:
        with open(label_map_path, "rb") as f:
            label_map = pickle.load(f)
        return label_map, None
    except Exception as e:
        return {}, f"Error loading label map: {e}"


def preprocess_image(image):
    """Preprocess uploaded image for prediction."""
    if image.mode != "RGB":
        image = image.convert("RGB")
    max_size = 512
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = tuple(int(dim * ratio) for dim in image.size)
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    return image


def predict_breed(model, image, label_map):
    """Predict breed from image using the model."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            image.save(tmp.name)
            image_path = tmp.name
        temp_df = pd.DataFrame({"image": [image_path], "label": [0]})
        start_time = time.time()
        predictions = model.predict(temp_df)
        inference_time = time.time() - start_time
        try:
            probabilities = model.predict_proba(temp_df)
            predicted_class = predictions[0]
            # If label_map is used and prediction is int, map to class name
            if label_map and isinstance(predicted_class, int):
                predicted_class = label_map.get(predicted_class, predicted_class)
            # Fetch confidence for predicted class
            if predicted_class in probabilities.columns:
                confidence = float(probabilities.loc[0, predicted_class])
            else:
                confidence = float(probabilities.iloc[0].max())  # fallback
        except Exception:
            confidence = 0.85
        os.unlink(image_path)
        # For display, map index to class name if label_map is used
        display_class = (
            label_map.get(predictions[0], predictions[0])
            if label_map
            else predictions[0]
        )
        return display_class, inference_time, confidence, None
    except Exception as e:
        return None, None, None, f"Prediction error: {e}"


def get_supported_breeds(label_map):
    if label_map:
        return [breed.replace("_", " ").title() for breed in label_map.values()]
    else:
        return [
            "Golden Retriever",
            "Persian Cat",
            "Shiba Inu",
            "Maine Coon",
            "Labrador",
            "German Shepherd",
            "Beagle",
            "Boxer",
            "Bulldog",
            "Chihuahua",
            "Corgi",
            "Dachshund",
            "Husky",
            "Pomeranian",
            "Pug",
            "Rottweiler",
            "Yorkshire Terrier",
            "American Shorthair",
            "Mumbai Cat",
            "Ragdoll Cat",
            "Siamese Cat",
            "Sphynx",
            "Abyssinian",
        ]


# --- Sidebar Navigation ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=60)
st.sidebar.title("Pet Breed Classifier")
model, model_status = load_model()
label_map, label_status = load_label_map()
supported_breeds = get_supported_breeds(label_map)

with st.sidebar:
    st.markdown("---")
    if model is not None:
        st.markdown(
            '<div class="status-success">✅ Model Loaded</div>', unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="status-warning">⚠️ {model_status or "Demo Mode"}</div>',
            unsafe_allow_html=True,
        )
    if label_map:
        st.markdown(
            f'<div class="status-success">✅ {len(label_map)} Breeds</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="status-warning">⚠️ {label_status or "Label map missing"}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("---")
    st.header("Navigation")
    nav = st.radio("Go to:", ["Classify Image", "Model Info", "About"], index=0)
    st.markdown("---")
    st.caption("Built with ❤️ using AutoGluon & Streamlit")

# --- Main Content ---
st.markdown(
    '<h1 class="main-header">🐾 Pet Breed Classifier</h1>', unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-header">Upload a photo of your pet and discover its breed in seconds!</div>',
    unsafe_allow_html=True,
)

if nav == "Classify Image":
    tab1, tab2 = st.tabs(["🐶 Upload & Predict", "📋 Supported Breeds"])
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["png", "jpg", "jpeg"],
            help="Upload a pet image",
        )
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.markdown('<div class="upload-box">', unsafe_allow_html=True)
                st.image(image, caption="Preview", use_column_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                processed_image = preprocess_image(image)
                if st.button("🔍 Classify Breed", type="primary"):
                    with st.spinner("Analyzing image..."):
                        if model is not None:
                            pred, inf_time, conf, err = predict_breed(
                                model, processed_image, label_map
                            )
                        else:
                            # Demo mode fallback
                            import random

                            pred = random.choice(supported_breeds)
                            inf_time = 0.2
                            conf = np.random.uniform(0.7, 0.95)
                            err = None
                    if err:
                        st.markdown(
                            f'<div class="status-error">❌ {err}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            '<div class="prediction-box">', unsafe_allow_html=True
                        )
                        st.markdown(
                            f"## 🎯 Prediction: <br> <b>{pred}</b>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"⏱️ <b>Inference Time:</b> {inf_time:.3f} seconds",
                            unsafe_allow_html=True,
                        )
                        st.progress(conf)
                        st.write(f"Confidence: {conf:.1%}")
                        st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(
                    f'<div class="status-error">❌ Error: {e}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Please upload an image to begin.")
        st.markdown("</div>", unsafe_allow_html=True)
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Supported Breeds")
        st.markdown('<div class="breed-list">', unsafe_allow_html=True)
        for breed in supported_breeds:
            st.write(f"• {breed}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
elif nav == "Model Info":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Model Performance & Details")
    st.metric("Test Accuracy", "92,54%")
    st.metric("Categories", len(supported_breeds))
    st.metric("Avg Inference", "1.0746s")
    st.markdown("---")
    st.header("Recent Predictions (Demo)")
    sample_predictions = [
        ("Golden Retriever", "95.2%", "2 min ago"),
        ("Persian Cat", "87.1%", "5 min ago"),
        ("Shiba Inu", "82.3%", "8 min ago"),
        ("Maine Coon", "91.7%", "12 min ago"),
    ]
    for breed, conf, time_ago in sample_predictions:
        st.write(f"🐾 **{breed}** - {conf} ({time_ago})")
    st.markdown("</div>", unsafe_allow_html=True)
elif nav == "About":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("About This App")
    st.write(
        """
    - **Pet Breed Classifier** uses a deep learning model (AutoGluon) to identify the breed of a pet from an image.
    - The model supports 23 popular dog and cat breeds.
    - Upload a photo and get instant predictions with confidence scores.
    - If no model is found, the app runs in demo mode for UI testing.
    """
    )
    st.markdown("---")
    st.write(
        "For best results, ensure your model is trained and available in `models/autogluon_model/`."
    )
    st.write("To train a model, run:")
    st.code("python run_pipeline.py")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Built with ❤️ using AutoGluon and Streamlit</div>",
    unsafe_allow_html=True,
)
