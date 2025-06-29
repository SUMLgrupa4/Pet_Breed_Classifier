#!/bin/bash

# Docker build script for Pet Breed Classifier
# This script validates the model exists and builds the Docker image

set -e  # Exit on any error

echo "Pet Breed Classifier - Docker Build Script"
echo "=========================================="

# Check if model exists
MODEL_PATH="models/autogluon_model"
if [ ! -d "$MODEL_PATH" ]; then
    echo "ERROR: Model directory not found at $MODEL_PATH"
    echo "Please train the model first using: python run_pipeline.py"
    exit 1
fi

# Check required model files
REQUIRED_FILES=("model.ckpt" "config.yaml" "df_preprocessor.pkl")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$MODEL_PATH/$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    echo "ERROR: Missing required model files: ${MISSING_FILES[*]}"
    echo "Please ensure the model is properly trained and saved"
    exit 1
fi

# Show model info
echo "SUCCESS: Model found and validated"
echo "Model directory: $MODEL_PATH"
echo "Model files:"
ls -la "$MODEL_PATH/"
echo "Model size: $(du -sh "$MODEL_PATH" | cut -f1)"

# Build Docker image
echo ""
echo "Building Docker image..."
docker build -t pet-breed-classifier .

if [ $? -eq 0 ]; then
    echo ""
    echo "SUCCESS: Docker image built successfully!"
    echo ""
    echo "To run the container:"
    echo "  docker run -p 8501:8501 pet-breed-classifier"
    echo ""
    echo "To test the model loading:"
    echo "  docker run --rm pet-breed-classifier python test_model_loading.py"
    echo ""
    echo "The app will be available at: http://localhost:8501"
else
    echo ""
    echo "ERROR: Docker build failed!"
    exit 1
fi 