import os
import pickle
import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from autogluon.multimodal import MultiModalPredictor

def evaluate_model(test_df, model_path=None):
    """Load model and evaluate performance on test set."""
    if model_path is None:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(BASE_DIR, 'models', 'autogluon_model')

    predictor = MultiModalPredictor.load(model_path)

    start_time = time.time()
    predictions = predictor.predict(test_df)
    inference_time = time.time() - start_time

    accuracy = accuracy_score(test_df['label'], predictions)
    precision = precision_score(test_df['label'], predictions, average='weighted')
    recall = recall_score(test_df['label'], predictions, average='weighted')
    f1 = f1_score(test_df['label'], predictions, average='weighted')

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'inference_time': inference_time,
        'avg_inference_time': inference_time / len(test_df),
        'predictions': predictions,
        'true_labels': test_df['label'].values,
        'class_labels': predictor.class_labels
    }


def generate_confusion_matrix(performance_metrics, save_path='outputs/confusion_matrix.png'):
    """Generate and save confusion matrix."""
    true = performance_metrics['true_labels']
    pred = performance_metrics['predictions']
    cm = confusion_matrix(true, pred)

    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix - Pet Breed Classification')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    return save_path


def generate_classification_report(performance_metrics, save_path='outputs/classification_report.txt', label_map_path="data/metadata/label_map.pkl"):
    true = performance_metrics['true_labels']
    pred = performance_metrics['predictions']

    if os.path.exists(label_map_path):
        with open(label_map_path, "rb") as f:
            label_map = pickle.load(f)
    else:
        print("[WARNING] Label map not found, using numeric labels")
        label_map = {}

    true_names = [label_map.get(int(i), str(i)) for i in true]
    pred_names = [label_map.get(int(i), str(i)) for i in pred]

    if label_map:
        categories = [label_map[k] for k in sorted(label_map.keys())]
    else:
        categories = list(map(str, sorted(set(true))))

    report = classification_report(true_names, pred_names, target_names=categories, digits=3)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    try:
        with open(save_path, 'w') as f:
            f.write("PET BREED CLASSIFICATION REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(report)
    except Exception as e:
        print(f"[ERROR] Could not save classification report: {e}")

    return save_path


def analyze_model_size(model_path='models/autogluon_model', save_path='outputs/model_analysis.txt'):
    """Analyze model size on disk."""
    try:
        total_size = 0
        file_count = 0

        for root, _, files in os.walk(model_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                total_size += file_size
                file_count += 1

        size_mb = total_size / (1024 ** 2)
        size_gb = size_mb / 1024

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w') as f:
            f.write("MODEL SIZE ANALYSIS\n")
            f.write("=" * 25 + "\n")
            f.write(f"Total files: {file_count}\n")
            f.write(f"Model size: {size_mb:.2f} MB ({size_gb:.2f} GB)\n")

        return {'file_count': file_count, 'size_mb': size_mb, 'size_gb': size_gb}

    except Exception as e:
        print(f"[ERROR] Model size analysis failed: {e}")
        return None


def final_model_assessment(performance_metrics, save_path='outputs/final_assessment.txt'):
    """Provide final assessment for production readiness."""
    accuracy = performance_metrics['accuracy']
    avg_inference_time = performance_metrics['avg_inference_time']
    precision = performance_metrics['precision']
    recall = performance_metrics['recall']
    f1 = performance_metrics['f1_score']

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    try:
        with open(save_path, 'w') as f:
            f.write("FINAL MODEL ASSESSMENT\n")
            f.write("=" * 25 + "\n\n")
            f.write(f"Accuracy:           {accuracy:.4f} ({accuracy * 100:.2f}%)\n")
            f.write(f"Precision (weighted): {precision:.4f}\n")
            f.write(f"Recall (weighted):    {recall:.4f}\n")
            f.write(f"F1 Score (weighted):  {f1:.4f}\n")
            f.write(f"Avg Inference Time:   {avg_inference_time:.4f} seconds\n")
    except Exception as e:
        print(f"[ERROR] Could not save final assessment: {e}")

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'avg_inference_time': avg_inference_time
    }