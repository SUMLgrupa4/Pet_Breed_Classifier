from scripts.preprocess import preprocess_data
from scripts.train_model import train_model
from scripts.validate_model import (
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
        print("   ❌ Data directory not found: data/pet_breeds/")
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
        print("   ❌ No images found in data/pet_breeds/")
        print("   Please add your training images to the appropriate breed directories.")
        return
    
    print(f"   ✅ Found {total_images} total images across all breeds")

    # Step 1: Preprocess data
    print(" Step 1: Preprocessing data...")
    train_df, val_df, test_df = preprocess_data(parameters)

    # Step 2: Train model
    print(" Step 2: Training model...")
    train_model(train_df, val_df, parameters)

    # Step 3: Evaluate model
    print(" Step 3: Evaluating model on test data...")
    performance_metrics = evaluate_model(test_df)

    # Step 4: Generate confusion matrix
    print(" Step 4: Generating confusion matrix...")
    generate_confusion_matrix(performance_metrics)

    # Step 5: Generate classification report
    print(" Step 5: Generating classification report...")
    generate_classification_report(performance_metrics)

    # Step 6: Analyze model size
    print(" Step 6: Analyzing model size...")
    analyze_model_size()

    # Step 7: Final assessment summary
    print(" Step 7: Final model assessment...")
    final_model_assessment(performance_metrics)

    print("\n Pipeline completed successfully! All outputs saved to 'outputs/' folder.\n")


if __name__ == "__main__":
    run_pipeline()
