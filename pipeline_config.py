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
            "num_trials": 5  # Reduced from 10 for faster training
        },
        "hyperparameters": {
            "model.names": ["timm_image"],
            "model.timm_image.checkpoint_name": ["resnet18", "resnet50"],  # Removed mobilenet for speed
            "optimization.learning_rate": [0.0001, 0.001],  # Reduced options
            "env.per_gpu_batch_size": [16, 32]  # Removed smaller batch size
        },
        "num_gpus": 0,
        "num_cpus": 8,
        "batch_size": 32,  # Increased for faster training
        "learning_rate": 0.001,  # Slightly higher for faster convergence
        "max_epochs": 50,  # Reduced from 100
        "patience": 10  # Reduced from 15
    }
}
