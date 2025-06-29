import os
import shutil
import pickle
import yaml
from autogluon.multimodal import MultiModalPredictor


def train_model(train_df, val_df, parameters):
    """
    Trains an AutoGluon MultiModalPredictor model for image classification.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(BASE_DIR, 'models')
    model_output_path = os.path.join(models_dir, 'autogluon_model')

    model_options = parameters["model_options"]

    # Ensure model directory exists
    os.makedirs(models_dir, exist_ok=True)

    if os.path.exists(model_output_path):
        shutil.rmtree(model_output_path)

    print(f"Starting model training with configuration:")
    print(f"   - Time limit: {model_options['time_limit']} seconds ({model_options['time_limit'] / 3600:.1f} hours)")
    print(f"   - Preset: {model_options['presets']}")
    print(f"   - Classes: {train_df['label'].nunique()}")

    # Print model architecture info
    if 'hyperparameters' in model_options:
        arch = model_options['hyperparameters'].get('model.timm_image.checkpoint_name', 'auto')
        print(f"   - Model architecture: {arch}")

    # Create and train the model
    predictor = MultiModalPredictor(
        label="label",
        path=model_output_path,
        eval_metric="accuracy",
        verbosity=2,
        problem_type="multiclass"
    )

    # Prepare fit arguments
    fit_kwargs = {
        'train_data': train_df,
        'tuning_data': val_df,
        'time_limit': model_options["time_limit"],
        'presets': model_options["presets"]
    }

    # Add hyperparameters if specified
    if 'hyperparameters' in model_options:
        fit_kwargs['hyperparameters'] = model_options['hyperparameters']

    # Add hyperparameter tuning if specified
    if 'hyperparameter_tune_kwargs' in model_options:
        fit_kwargs['hyperparameter_tune_kwargs'] = model_options['hyperparameter_tune_kwargs']

    predictor.fit(**fit_kwargs)

    print(f"Model training completed successfully!")
    print(f"Model saved to: {model_output_path}")

    # Save the model properly
    predictor.save(model_output_path)

    # Verify the saved model configuration
    verify_saved_model(model_output_path)

    # Create label map for inference
    create_label_map(train_df, model_output_path)

    return predictor


def verify_saved_model(model_path):
    """Verify that the saved model has the correct configuration."""
    config_path = os.path.join(model_path, 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        model_arch = config.get('model', {}).get('timm_image', {}).get('checkpoint_name', 'unknown')
        print(f"Saved model architecture: {model_arch}")

        # Check if model.ckpt exists
        model_ckpt = os.path.join(model_path, 'model.ckpt')
        if os.path.exists(model_ckpt):
            size_mb = os.path.getsize(model_ckpt) / (1024 * 1024)
            print(f"Model checkpoint size: {size_mb:.1f} MB")
        else:
            print("WARNING: model.ckpt not found!")
    else:
        print("WARNING: config.yaml not found!")


def create_label_map(train_df, model_path):
    """Create a label map for converting numeric labels back to breed names."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metadata_dir = os.path.join(BASE_DIR, 'data', 'metadata')
    os.makedirs(metadata_dir, exist_ok=True)

    # Get unique labels and their counts
    label_counts = train_df['label'].value_counts().sort_index()

    # Create a mapping from numeric index to original label names
    # We need to get the original label names from the data
    label_map = {}

    # Get the original label names from the training data
    # Since we factorized the labels in preprocess.py, we need to reconstruct
    unique_labels = sorted(train_df['label'].unique())

    # For now, create a simple mapping - in a real scenario, you'd want to preserve the original names
    for i, label_idx in enumerate(unique_labels):
        label_map[label_idx] = f"breed_{i}"

    # Save the label map
    label_map_path = os.path.join(metadata_dir, 'label_map.pkl')
    with open(label_map_path, 'wb') as f:
        pickle.dump(label_map, f)

    print(f"Label map saved to: {label_map_path}")
    print(f"Label map: {label_map}")

    return label_map