parameters = {
    "model_options": {
        "test_size": 0.2,
        "random_state": 42,
        "image_size": [224, 224],
        "augmentation": True,
        "time_limit": 18000,  # 5 hours
        "presets": "best_quality",
        "hyperparameter_tune_kwargs": {
            "scheduler": "local",
            "searcher": "random",
            "num_trials": 10,
        },
        "hyperparameters": {
            "model.names": ["timm_image"],
            "model.timm_image.checkpoint_name": [
                "resnet18",
                "resnet50",
                "mobilenetv3_small_100",
            ],
            "optimization.learning_rate": [0.0001, 0.0005, 0.001, 0.005],
            "env.per_gpu_batch_size": [8, 16, 32],
        },
        "num_gpus": 0,
        "num_cpus": 8,
        "batch_size": 16,
        "learning_rate": 0.0001,
        "max_epochs": 100,
        "patience": 15,
    }
}
