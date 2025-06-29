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

# Verify and validate the trained model
RUN echo "Checking for trained model..." && \
    if [ -d "models/autogluon_model" ]; then \
        echo "SUCCESS: Trained model directory found" && \
        ls -la models/autogluon_model/ && \
        if [ -f "models/autogluon_model/model.ckpt" ]; then \
            echo "SUCCESS: Model checkpoint found" && \
            echo "Model size: $(du -sh models/autogluon_model/model.ckpt | cut -f1)" && \
        else \
            echo "ERROR: Model checkpoint not found!" && \
            exit 1 && \
        fi && \
        if [ -f "models/autogluon_model/config.yaml" ]; then \
            echo "SUCCESS: Model config found" && \
        else \
            echo "ERROR: Model config not found!" && \
            exit 1 && \
        fi && \
        if [ -f "models/autogluon_model/df_preprocessor.pkl" ]; then \
            echo "SUCCESS: Data preprocessor found" && \
        else \
            echo "ERROR: Data preprocessor not found!" && \
            exit 1 && \
        fi && \
        echo "SUCCESS: All required model files found" && \
    else \
        echo "ERROR: No trained model found at models/autogluon_model/" && \
        echo "Please ensure the model is trained and available before building the Docker image" && \
        exit 1 && \
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