import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from PIL import Image
import matplotlib.pyplot as plt


def preprocess_data(parameters):
    """
    Scans the raw data directory, creates a DataFrame with image paths and labels,
    and splits it into training, validation, and test sets with improved data quality.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_data_path = os.path.join(BASE_DIR, 'data', 'pet_breeds')
    outputs_dir = os.path.join(BASE_DIR, 'outputs')
    splits_dir = os.path.join(BASE_DIR, 'data', 'splits')
    metadata_dir = os.path.join(BASE_DIR, 'data', 'metadata')

    # Debug: Print paths
    print(f"Debug Paths:")
    print(f"   __file__: {__file__}")
    print(f"   BASE_DIR: {BASE_DIR}")
    print(f"   raw_data_path: {raw_data_path}")
    print(f"   raw_data_path exists: {os.path.exists(raw_data_path)}")
    print(f"   Current working directory: {os.getcwd()}")

    # Check if we're in Docker
    in_docker = os.path.exists('/.dockerenv')
    print(f"   In Docker: {in_docker}")

    # List contents of data directory
    data_dir = os.path.join(BASE_DIR, 'data')
    if os.path.exists(data_dir):
        print(f"   Data directory contents: {os.listdir(data_dir)}")
    else:
        print(f"   ERROR: Data directory not found: {data_dir}")

    image_files = []

    print("Scanning raw data directory...")

    for dirpath, _, filenames in os.walk(raw_data_path):
        category = os.path.basename(dirpath)
        valid_images = 0

        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(dirpath, filename)

                # Validate image can be opened
                try:
                    with Image.open(image_path) as img:
                        # Check if image is valid and has reasonable dimensions
                        if img.size[0] > 10 and img.size[1] > 10:  # Reduced minimum size check from 50 to 10
                            image_files.append({
                                "image": image_path,
                                "label": category
                            })
                            valid_images += 1
                        else:
                            print(f"Image too small: {image_path} - {img.size}")
                except Exception as e:
                    print(f"Skipping invalid image {image_path}: {e}")
                    continue

        print(f"{category}: {valid_images} valid images")

    df = pd.DataFrame(image_files)

    if df.empty:
        raise ValueError("No valid images found in the raw data directory!")

    print(f"\n Dataset Summary:")
    print(f"   Total images: {len(df)}")
    print(f"   Categories: {df['label'].nunique()}")

    # Remove duplicates based on image path
    initial_count = len(df)
    df = df.drop_duplicates(subset=['image']).reset_index(drop=True)
    duplicates_removed = initial_count - len(df)
    print(f"   Duplicates removed: {duplicates_removed}")

    # Analyze class distribution
    class_counts = df['label'].value_counts()
    print(f"\n Class Distribution:")
    print(f"   Min samples per class: {class_counts.min()}")
    print(f"   Max samples per class: {class_counts.max()}")
    print(f"   Mean samples per class: {class_counts.mean():.1f}")
    print(f"   Std samples per class: {class_counts.std():.1f}")

    # Plot class distribution
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(splits_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)

    plt.figure(figsize=(12, 6))
    class_counts.sort_index().plot(kind='bar')
    plt.title("Class Distribution")
    plt.xlabel("Class Name")
    plt.ylabel("Number of Images")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, "class_distribution.png"))
    plt.close()

    # Save summary to file
    with open(os.path.join(outputs_dir, "preprocessing_summary.txt"), "w") as f:
        f.write("DATASET SUMMARY\n")
        f.write("======================\n")
        f.write(f"Total images: {len(df)}\n")
        f.write(f"Categories: {df['label'].nunique()}\n")
        f.write(f"Duplicates removed: {duplicates_removed}\n")
        f.write(f"Min samples/class: {class_counts.min()}\n")
        f.write(f"Max samples/class: {class_counts.max()}\n")
        f.write(f"Mean samples/class: {class_counts.mean():.1f}\n")
        f.write(f"Std samples/class: {class_counts.std():.1f}\n")

    # Check for class imbalance
    imbalance_ratio = class_counts.max() / class_counts.min()
    if imbalance_ratio > 3:
        print(f"Class imbalance detected (ratio: {imbalance_ratio:.1f})")
    else:
        print(f"Class distribution is relatively balanced")

    # Create label map before encoding
    unique_labels = sorted(df['label'].unique())
    label_map = {i: label for i, label in enumerate(unique_labels)}

    # Save label map
    label_map_path = os.path.join(metadata_dir, 'label_map.pkl')
    with open(label_map_path, 'wb') as f:
        pickle.dump(label_map, f)
    print(f"Label map saved to: {label_map_path}")
    print(f"Label map: {label_map}")

    # Encode labels
    df['label'] = pd.factorize(df['label'])[0]

    # First split to separate out the test set
    train_val_df, test_df = train_test_split(
        df,
        test_size=parameters["model_options"]["test_size"],
        random_state=parameters["model_options"]["random_state"],
        stratify=df["label"]
    )

    # Second split to create training and validation sets
    train_df, val_df = train_test_split(
        train_val_df,
        test_size=parameters["model_options"]["test_size"],
        random_state=parameters["model_options"]["random_state"],
        stratify=train_val_df["label"]
    )

    print(f"\n Final Split Summary:")
    print(f"   Training set: {len(train_df)} images")
    print(f"   Validation set: {len(val_df)} images")
    print(f"   Test set: {len(test_df)} images")

    # Save splits to disk
    train_df.to_csv(os.path.join(splits_dir, "train_data.csv"), index=False)
    val_df.to_csv(os.path.join(splits_dir, "val_data.csv"), index=False)
    test_df.to_csv(os.path.join(splits_dir, "test_data.csv"), index=False)

    print("Saved train/val/test data to data/splits/")

    return train_df, val_df, test_df