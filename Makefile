.PHONY: install train test deploy clean format update-branch hf-login push-hub

# Install dependencies
install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

# Train new model (only if you have new data)
train:
	python run_pipeline.py

# Use existing model (skip training)
use-existing:
	@echo "Using existing trained model..."
	@echo "Model found in models/autogluon_model/"
	@echo "Results found in outputs/"

# Quick evaluation with existing model
eval:
	echo "## Model Metrics" > report.md
	cat ./outputs/classification_report.txt >> report.md
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](./outputs/confusion_matrix.png)' >> report.md
	cml comment create report.md

# Quick evaluation without CML (if CML not available)
eval-simple:
	echo "## Model Metrics" > report.md
	cat ./outputs/classification_report.txt >> report.md
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](./outputs/confusion_matrix.png)' >> report.md
	@echo "Report generated: report.md"

# Setup development environment
setup:
	pip install -r requirements.txt
	mkdir -p data/images data/metadata outputs models

# Full pipeline: setup, train, test
pipeline: setup train test

# Deploy with existing model (recommended)
deploy: use-existing eval-simple hf-login push-hub

# Deploy with retraining (only if you have new data)
deploy-retrain: train eval hf-login push-hub

# Quick local test
test-local:
	streamlit run streamlit_app.py

# Clean up (be careful - this removes your trained model!)
clean:
	rm -rf outputs/*
	rm -rf models/autogluon_model/*
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Run the Streamlit app locally
run-app:
	streamlit run streamlit_app.py

# Setup development environment
setup:
	pip install -r requirements.txt
	mkdir -p data/images data/metadata outputs models

# Full pipeline: setup, train, test
pipeline: setup train test

# Help
help:
	@echo "Available commands:"
	@echo "  install         - Install dependencies"
	@echo "  format          - Format code with Black"
	@echo "  train           - Train new model (if you have new data)"
	@echo "  use-existing    - Use existing trained model"
	@echo "  eval            - Generate evaluation report with CML"
	@echo "  eval-simple     - Generate evaluation report without CML"
	@echo "  deploy          - Deploy with existing model (RECOMMENDED)"
	@echo "  deploy-retrain  - Deploy with retraining (only if new data)"
	@echo "  test-local      - Test Streamlit app locally"
	@echo "  clean           - Clean all generated files (CAREFUL!)"
	@echo "  help            - Show this help message"

format:
	black *.py

update-branch:
	git config --global user.name $(USER_NAME)
	git config --global user.email $(USER_EMAIL)
	git commit -am "Update with new results"
	git push --force origin HEAD:update

hf-login:
	git pull origin update
	git switch update
	pip install -U "huggingface_hub[cli]"
	huggingface-cli login --token $(HF) --add-to-git-credential

push-hub:
	huggingface-cli upload $(HF_USERNAME)/pet-breed-classifier ./streamlit_app.py app.py --repo-type=space --commit-message="Sync App files"
	huggingface-cli upload $(HF_USERNAME)/pet-breed-classifier ./models /models --repo-type=space --commit-message="Sync Model"
	huggingface-cli upload $(HF_USERNAME)/pet-breed-classifier ./outputs /outputs --repo-type=space --commit-message="Sync Results"
