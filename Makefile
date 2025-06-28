.PHONY: install format train eval eval-simple hf-login push-hub deploy deploy-retrain test-local clean help update-branch docker-build docker-push docker-run docker-train-ci docker-train-compose docker-train-compose-detached fetch-data

# Fast install for CI/CD (no AutoGluon)
install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

# Full install for app (with AutoGluon)
install-app:
	pip install --upgrade pip &&\
	pip install -r requirements-app.txt

format:
	black *.py

# Data fetching
fetch-data:
	python scripts/fetch_data.py

train:
	python run_pipeline.py

eval:
	echo "## Model Metrics" > report.md
	cat ./outputs/classification_report.txt >> report.md
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](./outputs/confusion_matrix.png)' >> report.md
	@echo "Report generated: report.md"

eval-simple:
	echo "## Model Metrics" > report.md
	cat ./outputs/classification_report.txt >> report.md
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](./outputs/confusion_matrix.png)' >> report.md
	@echo "Report generated: report.md"

hf-login:
	pip install -U "huggingface_hub[cli]"
	huggingface-cli login --token $(HF) --add-to-git-credential

push-hub:
	huggingface-cli upload $(HF_USERNAME)/pet-breed-classifier .app.py  --repo-type=space --commit-message="Sync App files"
	huggingface-cli upload $(HF_USERNAME)/pet-breed-classifier ./models models --repo-type=space --commit-message="Sync Model"
	huggingface-cli upload $(HF_USERNAME)/pet-breed-classifier ./outputs outputs --repo-type=space --commit-message="Sync Results"

deploy: hf-login push-hub

deploy-retrain: train eval hf-login push-hub

# Docker commands
docker-build:
	docker build -t pet-breed-classifier:latest .

docker-build-training:
	docker build -f Dockerfile.training -t pet-breed-classifier:training-data .

docker-push:
	docker tag pet-breed-classifier:latest $(DOCKER_USERNAME)/pet-breed-classifier:latest
	docker push $(DOCKER_USERNAME)/pet-breed-classifier:latest

docker-push-training:
	docker tag pet-breed-classifier:training-data $(DOCKER_USERNAME)/pet-breed-classifier:training-data
	docker push $(DOCKER_USERNAME)/pet-breed-classifier:training-data

docker-run:
	docker run -p 8501:8501 pet-breed-classifier:latest

docker-run-training:
	docker run -it --rm pet-breed-classifier:training-data python run_pipeline.py

docker-train-ci:
	docker run --rm -v $(PWD)/data:/app/data -v $(PWD)/models:/app/models -v $(PWD)/outputs:/app/outputs pet-breed-classifier:training-data python run_pipeline.py

docker-train-compose:
	docker-compose -f docker-compose.training.yml up --build

docker-train-compose-detached:
	docker-compose -f docker-compose.training.yml up -d --build

test-local:
	streamlit run app.py

clean:
	rm -rf outputs/*
	rm -rf models/autogluon_model/*
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

use-existing:
	@echo "Using existing trained model..."
	@echo "Model found in models/autogluon_model/"
	@echo "Results found in outputs/"

help:
	@echo "Available commands:"
	@echo "  install         - Install dependencies"
	@echo "  install-app     - Full install (with AutoGluon) - for local"
	@echo "  format          - Format code with Black"
	@echo "  fetch-data      - Fetch training data from Hugging Face"
	@echo "  train           - Train new model (if you have new data)"
	@echo "  use-existing    - Use existing trained model"
	@echo "  eval            - Generate evaluation report with CML"
	@echo "  eval-simple     - Generate evaluation report without CML"
	@echo "  deploy          - Deploy with existing model (RECOMMENDED)"
	@echo "  deploy-retrain  - Deploy with retraining (only if new data)"
	@echo "  docker-build    - Build Docker image"
	@echo "  docker-build-training - Build Docker image for training"
	@echo "  docker-push     - Push Docker image to registry"
	@echo "  docker-push-training - Push training Docker image to registry"
	@echo "  docker-run      - Run Docker container"
	@echo "  docker-run-training - Run training in Docker container"
	@echo "  docker-train-ci  - Run training in Docker container for CI"
	@echo "  docker-train-compose - Run training in Docker container for CI using docker-compose"
	@echo "  docker-train-compose-detached - Run training in Docker container for CI using docker-compose in detached mode"
	@echo "  test-local      - Test Streamlit app locally"
	@echo "  clean           - Clean all generated files (CAREFUL!)"
	@echo "  help            - Show this help message"
