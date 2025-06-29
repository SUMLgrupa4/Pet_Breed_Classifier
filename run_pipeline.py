from scripts.preprocess import preprocess_data
from scripts.train_model import train_model
from scripts.validate_model import (
    validate_model_loading,
    evaluate_model,
    generate_confusion_matrix,
    generate_classification_report,
    analyze_model_size,
    final_model_assessment
)
from pipeline_config import parameters
import os


def run_pipeline():
    print("\n Starting Full Training & Evaluation Pipeline...\n")

    # Step 0: Check for local training data
    print(" Step 0: Checking for local training data...")
    data_dir = os.path.join(os.path.dirname(__file__), 'data', 'pet_breeds')
    
    if not os.path.exists(data_dir):
        print("   ERROR: Data directory not found: data/pet_breeds/")
        print("   Please ensure your training data is in the data/pet_breeds/ directory.")
        return
    
    # Count images in each breed directory
    total_images = 0
    for breed_dir in os.listdir(data_dir):
        breed_path = os.path.join(data_dir, breed_dir)
        if os.path.isdir(breed_path):
            images = [f for f in os.listdir(breed_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            total_images += len(images)
            print(f"   {breed_dir}: {len(images)} images")
    
    if total_images == 0:
        print("   ERROR: No images found in data/pet_breeds/")
        print("   Please add your training images to the appropriate breed directories.")
        return
    
    print(f"   SUCCESS: Found {total_images} total images across all breeds")

    # Step 1: Preprocess data
    print(" Step 1: Preprocessing data...")
    train_df, val_df, test_df = preprocess_data(parameters)

    # Step 2: Train model
    print(" Step 2: Training model...")
    train_model(train_df, val_df, parameters)

    # Step 3: Validate trained model
    print(" Step 3: Validating trained model...")
    if not validate_model_loading():
        print("   ERROR: Model validation failed!")
        print("   The trained model cannot be loaded correctly.")
        return
    print("   SUCCESS: Model validation passed!")

    # Step 4: Evaluate model
    print(" Step 4: Evaluating model on test data...")
    performance_metrics = evaluate_model(test_df)

    # Step 5: Generate confusion matrix
    print(" Step 5: Generating confusion matrix...")
    generate_confusion_matrix(performance_metrics)

    # Step 6: Generate classification report
    print(" Step 6: Generating classification report...")
    generate_classification_report(performance_metrics)

    # Step 7: Analyze model size
    print(" Step 7: Analyzing model size...")
    analyze_model_size()

    # Step 8: Final assessment summary
    print(" Step 8: Final model assessment...")
    final_model_assessment(performance_metrics)

    print("\n Pipeline completed successfully! All outputs saved to 'outputs/' folder.\n")


if __name__ == "__main__":
    run_pipeline()
