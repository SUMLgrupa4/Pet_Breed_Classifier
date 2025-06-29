# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

# Copy project files (excluding what's in .dockerignore)
COPY . .

# Create necessary directories
RUN mkdir -p \
    data/metadata \
    models \
    outputs

# Check for trained model and set demo mode if not available
RUN echo "Checking for trained model..." && \
    if [ -d "models/autogluon_model" ] && [ -f "models/autogluon_model/config.yaml" ] && [ -f "models/autogluon_model/df_preprocessor.pkl" ]; then \
        echo "SUCCESS: Trained model directory found" && \
        ls -la models/autogluon_model/ && \
        echo "SUCCESS: Model config found" && \
        echo "SUCCESS: Data preprocessor found" && \
        echo "SUCCESS: All required model files found" && \
        echo "DEMO_MODE=false" > /app/demo_mode.txt && \
        echo "Running in FULL MODE with trained model" && \
    else \
        echo "WARNING: No trained model found at models/autogluon_model/" && \
        echo "Running in DEMO MODE - will use placeholder model" && \
        echo "DEMO_MODE=true" > /app/demo_mode.txt && \
        echo "To use full model, ensure model artifacts are available during build" && \
    fi

# Add non-root user for security
RUN useradd -m streamlit && \
    chown -R streamlit:streamlit /app
USER streamlit

# Expose port for Streamlit
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"] 