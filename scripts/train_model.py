import os
import shutil
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

    print(f"Starting model training with MAXIMUM QUALITY configuration:")
    print(f"   - Time limit: {model_options['time_limit']} seconds ({model_options['time_limit']/3600:.1f} hours)")
    print(f"   - Preset: {model_options['presets']}")
    print(f"   - Classes: {train_df['label'].nunique()}")

    # Create and train the model
    predictor = MultiModalPredictor(
        label="label",
        path=model_output_path,
        eval_metric="accuracy",
        verbosity=2,
        problem_type="multiclass"
    )

    predictor.fit(
        train_data=train_df,
        tuning_data=val_df,
        time_limit=model_options["time_limit"],
        presets=model_options["presets"]
    )

    print(f"Model training completed successfully!")
    print(f"Model saved to: {model_output_path}")

    predictor.save(model_output_path)
    return predictor