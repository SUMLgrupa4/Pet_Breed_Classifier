import os
import pickle
from pathlib import Path

def create_label_map_from_folders(pet_breeds_path):
    """
    Create label map from folder names in pet_breeds directory.
    """
    # Create metadata directory
    os.makedirs("data/metadata", exist_ok=True)
    
    # Get all subdirectories (breed folders)
    breed_folders = []
    if os.path.exists(pet_breeds_path):
        for item in os.listdir(pet_breeds_path):
            item_path = os.path.join(pet_breeds_path, item)
            if os.path.isdir(item_path):
                breed_folders.append(item)
    
    if not breed_folders:
        print(f"No breed folders found in {pet_breeds_path}")
        return
    
    # Sort folders to ensure consistent ordering
    breed_folders.sort()
    
    # Create label map
    label_map = {}
    for i, breed_folder in enumerate(breed_folders):
        # Convert folder name to readable breed name
        breed_name = breed_folder.replace('_', ' ').title()
        label_map[i] = breed_name
    
    # Save label map
    label_map_path = "data/metadata/label_map.pkl"
    with open(label_map_path, "wb") as f:
        pickle.dump(label_map, f)
    
    print(f"✅ Created label map with {len(label_map)} breeds")
    print(f"📁 Saved to: {label_map_path}")
    print("\n📋 Breeds in your model:")
    for k, v in label_map.items():
        print(f"   {k}: {v}")
    
    return label_map

if __name__ == "__main__":
    # Try different possible paths
    possible_paths = [
        "data/pet_breeds/pet_breeds",  # Updated to correct path
        "pet_breeds",
        "data/pet_breeds", 
        "../pet_breeds",
        "extracted_pet_breeds"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found pet breeds folder at: {path}")
            create_label_map_from_folders(path)
            break
    else:
        print("❌ Could not find pet_breeds folder!")
        print("Please extract pet_breeds.zip and run this script again.")
        print("\nExpected folder structure:")
        print("pet_breeds/")
        print("├── golden_retriever/")
        print("├── persian_cat/")
        print("└── ...") 