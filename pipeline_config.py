parameters = {
    "model_options": {
        "test_size": 0.2,
        "random_state": 42,
        "image_size": [224, 224],
        "augmentation": True,
        "time_limit": 1800,  # 30 min for CI/CD
        "presets": "medium_quality",  # Faster than best_quality for CI
        "hyperparameter_tune_kwargs": {
            "scheduler": "local",
            "searcher": "random",
            "num_trials": 3  # Reduced for faster training
        },
        "hyperparameters": {
            "model.names": ["timm_image"],
            "model.timm_image.checkpoint_name": "mobilenetv3_large_100",  # Fixed to match saved model
            "optimization.learning_rate": 0.0004,  # Fixed to match saved model
            "env.per_gpu_batch_size": 8  # Fixed to match saved model
        },
        "num_gpus": 0,
        "num_cpus": 8,
        "batch_size": 128,  # Fixed to match saved model
        "learning_rate": 0.0004,  # Fixed to match saved model
        "max_epochs": 10,  # Fixed to match saved model
        "patience": 10
    }
}
