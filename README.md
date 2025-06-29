---
title: Pet Breed Classifier
emoji: 🐾
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
license: mit
python_version: "3.9"
---

# Pet Breed Classifier 🐾

A machine learning model that classifies pet breeds from images using AutoGluon and Streamlit. This project includes a complete CI/CD pipeline for automated training and deployment.

## 🚀 Features

- **23 Pet Breeds**: Classify popular dog and cat breeds
- **High Accuracy**: 92.54% overall accuracy
- **Fast Inference**: Real-time predictions with confidence scores
- **Beautiful UI**: Modern Streamlit interface
- **CI/CD Pipeline**: Automated training and deployment
- **Training Results**: Confusion matrix, classification reports, and model analysis

## 📊 Model Performance

- **Overall Accuracy**: 92.54%
- **Average Precision**: 0.92
- **Average Recall**: 0.91
- **Average F1-Score**: 0.91
- **Supported Breeds**: 23 (Dogs & Cats)

## 🛠️ Technologies

- **AutoGluon**: Multi-modal deep learning framework
- **Streamlit**: Web application framework
- **Python 3.9+**: Core programming language
- **GitHub Actions**: CI/CD automation
- **Docker**: Containerization

## 📁 Project Structure

```
Pet_Breed_Classifier-master/
├── .github/workflows/          # CI/CD workflows
│   ├── train-and-deploy.yml    # Training and deployment workflow
│   ├── tests.yml               # Testing workflow
│   ├── ci.yml                  # Continuous integration
│   └── cd.yml                  # Continuous deployment
├── scripts/                    # Training scripts
│   ├── preprocess.py           # Data preprocessing
│   ├── train_model.py          # Model training
│   ├── validate_model.py       # Model validation
│   └── fetch_data.py           # Data fetching
├── models/                     # Trained models
├── outputs/                    # Training results
├── data/                       # Training data
│   ├── pet_breeds/             # Pet images by breed
│   └── metadata/               # Labels and metadata
├── app.py                      # Web application
├── run_pipeline.py             # Complete training pipeline
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker configuration
├── Dockerfile.optimized        # Optimized Docker image
├── Dockerfile.production       # Production Docker image
└── README.md                   # This file
```

## 🚀 Quick Start

### Option 1: GitHub Actions (Recommended)

1. **Push to GitHub** - The workflows will run automatically
2. **Set up secrets** (see Setup section below)
3. **Monitor progress** in the Actions tab

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Pet_Breed_Classifier-master
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Fetch training data**
   ```bash
   python scripts/fetch_data.py
   ```

4. **Run the training pipeline**
   ```bash
   python run_pipeline.py
   ```

5. **Launch the Streamlit app**
   ```bash
   streamlit run app.py
   ```

### Option 3: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run with Docker directly
docker build -f Dockerfile.production -t pet-breed-classifier .
docker run -p 8501:8501 pet-breed-classifier
```

## 🔧 Setup

### GitHub Actions Setup

1. **Add GitHub Secrets**
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `KAGGLE_USERNAME`: Your Kaggle username
     - `KAGGLE_KEY`: Your Kaggle API key
     - `DOCKER_USERNAME`: Your Docker Hub username
     - `DOCKER_PASSWORD`: Your Docker Hub password/token

2. **Trigger Workflows**
   - **Automatic**: Push to `main` or `develop` branch
   - **Manual**: Go to Actions tab → Select workflow → Run workflow

### Available Workflows

#### 1. **Model Training and Deployment** (`train-and-deploy.yml`)
- ✅ Fetches training data from Kaggle
- ✅ Trains the model using your pipeline
- ✅ Builds Docker image with trained model
- ✅ Saves artifacts for later use

#### 2. **Basic Tests** (`tests.yml`)
- ✅ Tests all imports (Streamlit, PyTorch, AutoGluon)
- ✅ Tests data fetching functionality
- ✅ Tests preprocessing pipeline
- ✅ Tests Docker build process
- ✅ Validates app functionality

## 🐳 Docker Images

### Available Dockerfiles

- **`Dockerfile.optimized`**: Space-efficient build with multi-stage optimization
- **`Dockerfile.production`**: Production-ready with security features
- **`Dockerfile.training`**: Training-specific with all dependencies

### Building Images

```bash
# Optimized build (recommended)
docker build -f Dockerfile.optimized -t pet-breed-classifier:latest .

# Production build
docker build -f Dockerfile.production -t pet-breed-classifier:prod .

# Training build
docker build -f Dockerfile.training -t pet-breed-classifier:training .
```

### Running Containers

```bash
# Run with volume mounts (recommended)
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/outputs:/app/outputs \
  --name pet-breed-classifier \
  pet-breed-classifier:latest

# Run with Docker Compose
docker-compose up --build -d
```

## 📈 Training Results

After each training run, the following artifacts are generated:

### 📊 Confusion Matrix
- Visual representation of model predictions vs actual labels
- Helps identify which breeds are most/least accurately classified

### 📋 Classification Report
- Detailed precision, recall, and F1-score for each breed
- Overall model performance metrics

### 📊 Model Analysis
- Model size and complexity analysis
- Training time and resource usage

### 🎯 Final Assessment
- Summary of model performance
- Recommendations for improvement

## 🔍 Troubleshooting

### Common Issues

1. **"No space left on device"**
   - ✅ Fixed! Use `Dockerfile.optimized` for smaller images
   - ✅ Added `.dockerignore` to reduce build context

2. **"Module not found: scripts"**
   - ✅ Fixed! Updated `PYTHONPATH` in Dockerfiles
   - ✅ Removed `scripts/` from `.dockerignore`

3. **Dependency conflicts**
   - ✅ Fixed! Updated `requirements.txt` with compatible versions
   - ✅ Added version ranges to prevent conflicts

### Getting Help

1. Check the **Actions** tab for detailed error logs
2. Verify all required files are present
3. Ensure GitHub secrets are properly configured
4. Use the test workflow to validate your setup

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🎉 Ready to classify some pets? Push your code and watch the magic happen!** 🚀 