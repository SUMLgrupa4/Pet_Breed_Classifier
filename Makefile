.PHONY: install format train eval eval-simple hf-login push-hub deploy deploy-retrain test-local clean help

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

train:
	python run_pipeline.py

eval:
	echo "## Model Metrics" > report.md
	cat ./outputs/classification_report.txt >> report.md
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](./outputs/confusion_matrix.png)' >> report.md
	cml comment create report.md

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
	huggingface-cli upload $(HF_USERNAME)/pet-breed-classifier ./app.py app.py --repo-type=space --commit-message="Sync App files"
	huggingface-cli upload $(HF_USERNAME)/pet-breed-classifier ./requirements.txt requirements.txt --repo-type=space --commit-message="Sync Requirements"
	huggingface-cli upload $(HF_USERNAME)/pet-breed-classifier ./models models --repo-type=space --commit-message="Sync Model"
	huggingface-cli upload $(HF_USERNAME)/pet-breed-classifier ./outputs outputs --repo-type=space --commit-message="Sync Results"

deploy: use-existing eval-simple hf-login push-hub

deploy-retrain: train eval hf-login push-hub

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
	@echo "  train           - Train new model (if you have new data)"
	@echo "  use-existing    - Use existing trained model"
	@echo "  eval            - Generate evaluation report with CML"
	@echo "  eval-simple     - Generate evaluation report without CML"
	@echo "  deploy          - Deploy with existing model (RECOMMENDED)"
	@echo "  deploy-retrain  - Deploy with retraining (only if new data)"
	@echo "  test-local      - Test Streamlit app locally"
	@echo "  clean           - Clean all generated files (CAREFUL!)"
	@echo "  help            - Show this help message"
