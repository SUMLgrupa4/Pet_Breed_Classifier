#!/bin/bash

# Pet Breed Classifier - Docker Setup Script
# This script helps set up and run the Docker-based training pipeline

set -e

echo "🐾 Pet Breed Classifier - Docker Setup"
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo "✅ Python is installed"

# Install required Python packages for data fetching
echo "📦 Installing Python dependencies for data fetching..."
pip install datasets huggingface_hub

# Fetch training data from Hugging Face
echo "📥 Fetching training data from Hugging Face..."
python scripts/fetch_data.py

# Check if data directory exists and has content
if [ ! -d "data/pet_breeds" ] || [ -z "$(ls -A data/pet_breeds 2>/dev/null)" ]; then
    echo "⚠️  Warning: data/pet_breeds directory is empty or not found."
    echo "   Please ensure your training data is available."
    echo "   Continuing anyway..."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/pet_breeds data/metadata data/splits models outputs

echo "🔨 Building training Docker image..."
docker build -f Dockerfile.training -t pet-breed-classifier:training-data .

echo "🚀 Starting training pipeline..."
echo "   This may take a while depending on your data size and hardware."
echo "   You can monitor progress in the logs above."

# Run training pipeline
docker run --rm \
    -v "$(pwd)/data:/app/data" \
    -v "$(pwd)/models:/app/models" \
    -v "$(pwd)/outputs:/app/outputs" \
    pet-breed-classifier:training-data python run_pipeline.py

echo ""
echo "✅ Training completed!"
echo "📊 Check the outputs/ directory for results:"
echo "   - outputs/confusion_matrix.png"
echo "   - outputs/classification_report.txt"
echo "   - outputs/model_analysis.txt"
echo "   - outputs/final_assessment.txt"

echo ""
echo "🔨 Building production Docker image..."
docker build -t pet-breed-classifier:latest .

echo ""
echo "🎉 Setup complete!"
echo "📱 To run the application locally:"
echo "   docker run -p 8501:8501 pet-breed-classifier:latest"
echo ""
echo "🌐 Or use Docker Compose:"
echo "   docker-compose up --build" 