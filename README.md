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

A machine learning model that classifies pet breeds from images using AutoGluon and Streamlit. This project includes a complete CI/CD pipeline for automated training and deployment to Hugging Face Spaces.

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
- **Hugging Face Spaces**: Model deployment platform

## 📁 Project Structure

```
Pet_Breed_Classifier-master/
├── .github/workflows/          # CI/CD workflows
│   ├── deploy.yml              # Main deployment workflow
│   └── train-only.yml          # Training-only workflow
├── scripts/                    # Training scripts
│   ├── preprocess.py           # Data preprocessing
│   ├── train_model.py          # Model training
│   └── validate_model.py       # Model validation
├── models/                     # Trained models
├── outputs/                    # Training results
│   ├── confusion_matrix.png    # Confusion matrix visualization
│   ├── classification_report.txt
│   ├── model_analysis.txt
│   └── final_assessment.txt
├── app.py                      # Web application
├── run_pipeline.py             # Complete training pipeline
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker configuration
├── Dockerfile                  # Docker image
└── README.md                   # This file
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Pet_Breed_Classifier-master
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your training data**
   ```
   data/
   ├── images/                  # Your pet images
   └── metadata/                # Labels and metadata
   ```

4. **Run the training pipeline**
   ```bash
   python run_pipeline.py
   ```

5. **Launch the Streamlit app**
   ```bash
   streamlit run app.py
   ```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run with Docker directly
docker build -t pet-breed-classifier .
docker run -p 8501:8501 pet-breed-classifier
```

### CI/CD Deployment

#### Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **Hugging Face Account**: Create an account at [huggingface.co](https://huggingface.co)
3. **Hugging Face Token**: Generate a token with write permissions
4. **Docker Hub Account**: Create an account at [hub.docker.com](https://hub.docker.com)

#### Setup Steps

1. **Add GitHub Secrets**
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `HF_TOKEN`: Your Hugging Face token
     - `DOCKER_USERNAME`: Your Docker Hub username
     - `DOCKER_PASSWORD`: Your Docker Hub password/token

2. **Trigger Deployment**
   - **Automatic**: Push to `main` or `master` branch
   - **Manual**: Go to Actions tab → "Continuous Integration" → Run workflow
   - **Training Only**: Go to Actions tab → "Train Model Only" → Run workflow

3. **Access Your App**
   - Your app will be available at: `https://huggingface.co/spaces/<your-username>/pet-breed-classifier`

### Docker-Based CI Pipeline

The project now includes a comprehensive Docker-based CI pipeline that:

1. **Fetches Training Data**: Downloads the pet breed dataset from Hugging Face
2. **Builds Training Image**: Creates a Docker image with all training dependencies
3. **Runs Training Pipeline**: Executes the complete training pipeline in a containerized environment
4. **Builds Production Image**: Creates a production-ready image with the trained model
5. **Pushes to Registry**: Registers both training and production images to Docker Hub
6. **Deploys to Hugging Face**: Deploys the application with the latest model

#### Data Fetching

The CI pipeline automatically fetches training data from Hugging Face datasets:

```bash
# Fetch data manually
make fetch-data

# Or run the script directly
python scripts/fetch_data.py
```

The data fetching script:
- Attempts to load from multiple possible dataset names
- Falls back to creating a sample dataset if the main dataset is unavailable
- Creates the proper directory structure expected by the training pipeline
- Generates the label mapping file automatically

#### Docker Images

- **Training Image** (`pet-breed-classifier:training-data`): Contains all dependencies for model training
- **Production Image** (`pet-breed-classifier:latest`): Optimized for serving the trained model

#### Local Docker Training

```bash
# Fetch data and build training image
make fetch-data
make docker-build-training

# Run training pipeline
make docker-train-ci

# Or use docker-compose for training
make docker-train-compose
```

#### Docker Registry Integration

The CI pipeline automatically:
- Builds and pushes training images to Docker Hub
- Tags images with appropriate versions
- Maintains separate images for training and production
- Ensures reproducible training environments

## 📈 Training Results

After each training run, the following artifacts are generated:

### 📊 Confusion Matrix
- Visual representation of model predictions vs actual labels
- Helps identify which breeds are most/least accurately classified

### 📋 Classification Report
- Detailed per-class metrics (precision, recall, F1-score)
- Overall accuracy and macro/micro averages

### 📝 Model Analysis
- Model size and complexity analysis
- Training time and resource usage

### ✅ Final Assessment
- Summary of model performance
- Deployment readiness evaluation

## 🔧 Configuration

### Training Parameters
Edit `pipeline_config.py` to customize:
- Model architecture
- Training hyperparameters
- Data preprocessing settings
- Validation split ratios

### CI/CD Settings
Modify `.github/workflows/deploy.yml` to:
- Change deployment triggers
- Adjust resource allocation
- Customize deployment settings

## 📱 Using the App

1. **Upload Image**: Click "Browse files" to upload a pet image
2. **Get Prediction**: Click "Classify Breed" for instant results
3. **View Results**: See breed prediction with confidence score
4. **Check Performance**: Navigate to "Model Info" for detailed metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AutoGluon team for the excellent multi-modal framework
- Streamlit for the beautiful web app framework
- Hugging Face for providing free model hosting
- The open-source community for inspiration and support

---

**Built with ❤️ using AutoGluon & Streamlit**

*For questions or support, please open an issue on GitHub.* 