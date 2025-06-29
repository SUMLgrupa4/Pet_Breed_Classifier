import os
import shutil
import pickle
from pathlib import Path
import urllib.request
import zipfile
import tempfile

try:
    from datasets import load_dataset
    from huggingface_hub import hf_hub_download

    HF_AVAILABLE = True
except ImportError:
    print("⚠️  Hugging Face libraries not available. Using fallback methods.")
    HF_AVAILABLE = False

try:
    from kaggle.api.kaggle_api_extended import KaggleApi

    KAGGLE_AVAILABLE = True
except ImportError:
    print("⚠️  Kaggle API not available. Using fallback methods.")
    KAGGLE_AVAILABLE = False


def fetch_pet_breed_dataset():
    """
    Fetch the pet breed dataset from Kaggle.
    This function downloads the dataset and organizes it into the expected directory structure.
    """
    BASE_DIR = Path(__file__).parent.parent
    data_dir = BASE_DIR / "data"
    pet_breeds_dir = data_dir / "pet_breeds"
    metadata_dir = data_dir / "metadata"

    # Create necessary directories
    pet_breeds_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

    print("🐾 Fetching Pet Breed Dataset from Kaggle...")

    if KAGGLE_AVAILABLE:
        return fetch_from_kaggle()
    else:
        print("   Kaggle API not available, trying fallback methods...")
        return create_sample_dataset()


def fetch_from_kaggle():
    """
    Download the pet breed dataset from Kaggle using the Kaggle API.
    """
    try:
        # Initialize Kaggle API
        api = KaggleApi()

        # Try to authenticate using environment variables first (for Docker)
        kaggle_username = os.getenv('KAGGLE_USERNAME')
        kaggle_key = os.getenv('KAGGLE_KEY')

        if kaggle_username and kaggle_key:
            print("🔑 Using Kaggle credentials from environment variables...")
            # Create kaggle.json from environment variables
            import json
            kaggle_config = {
                "username": kaggle_username,
                "key": kaggle_key
            }

            # Create .kaggle directory and config file
            kaggle_dir = Path.home() / '.kaggle'
            kaggle_dir.mkdir(exist_ok=True)
            kaggle_config_file = kaggle_dir / 'kaggle.json'

            with open(kaggle_config_file, 'w') as f:
                json.dump(kaggle_config, f)

            # Set proper permissions
            os.chmod(kaggle_config_file, 0o600)

            api.authenticate()
        else:
            print("🔑 Using Kaggle credentials from ~/.kaggle/kaggle.json...")
            api.authenticate()

        print("✅ Kaggle API authenticated successfully!")

        # Download the dataset
        dataset_name = "aseemdandgaval/23-pet-breeds-image-classification"
        print(f"📥 Downloading dataset: {dataset_name}")

        # Create a temporary directory for the download
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download the dataset
            api.dataset_download_files(dataset_name, path=temp_dir, unzip=True)

            print("✅ Dataset downloaded and extracted successfully!")

            # Find the extracted directory
            extracted_dirs = [d for d in Path(temp_dir).iterdir() if d.is_dir()]
            if not extracted_dirs:
                print("❌ No extracted directories found")
                return create_sample_dataset()

            # Use the first extracted directory
            source_dir = extracted_dirs[0]
            print(f"📁 Found extracted data in: {source_dir}")

            # Organize the data into the expected structure
            return organize_kaggle_data(source_dir)

    except Exception as e:
        print(f"❌ Error downloading from Kaggle: {e}")
        print("   Falling back to sample dataset creation...")
        return create_sample_dataset()


def organize_kaggle_data(source_dir):
    """
    Organize the downloaded Kaggle data into the expected directory structure.
    """
    BASE_DIR = Path(__file__).parent.parent
    data_dir = BASE_DIR / "data"
    pet_breeds_dir = data_dir / "pet_breeds"
    metadata_dir = data_dir / "metadata"

    print("📁 Organizing Kaggle data...")

    # Look for the images directory
    images_dir = None
    for item in source_dir.iterdir():
        if item.is_dir() and any(name in item.name.lower() for name in ['image', 'train', 'data']):
            images_dir = item
            break

    if not images_dir:
        print("❌ Could not find images directory in downloaded data")
        return create_sample_dataset()

    print(f"📸 Found images in: {images_dir}")

    # Get all breed directories
    breed_dirs = [d for d in images_dir.iterdir() if d.is_dir()]

    if not breed_dirs:
        print("❌ No breed directories found")
        return create_sample_dataset()

    print(f"🐕 Found {len(breed_dirs)} breed directories")

    # Create label mapping
    breed_names = sorted([d.name for d in breed_dirs])
    label_map = {i: breed for i, breed in enumerate(breed_names)}

    # Save label map
    label_map_path = metadata_dir / "label_map.pkl"
    with open(label_map_path, "wb") as f:
        pickle.dump(label_map, f)
    print(f"✅ Label map saved to {label_map_path}")

    # Copy images to the expected structure
    total_images = 0
    for breed_dir in breed_dirs:
        breed_name = breed_dir.name
        target_dir = pet_breeds_dir / breed_name
        target_dir.mkdir(exist_ok=True)

        # Copy all image files
        image_files = list(breed_dir.glob("*.jpg")) + list(breed_dir.glob("*.jpeg")) + list(breed_dir.glob("*.png"))

        for i, image_file in enumerate(image_files):
            target_file = target_dir / f"image_{i:06d}{image_file.suffix}"
            shutil.copy2(image_file, target_file)

        total_images += len(image_files)
        print(f"   {breed_name}: {len(image_files)} images")

    print(f"✅ Dataset organized successfully!")
    print(f"   Total images: {total_images}")
    print(f"   Breeds: {len(breed_names)}")
    print(f"   Images saved to: {pet_breeds_dir}")

    return True


def create_sample_dataset():
    """
    Create a minimal sample dataset for testing purposes.
    This is used as a fallback when the main dataset is not available.
    """
    BASE_DIR = Path(__file__).parent.parent
    data_dir = BASE_DIR / "data"
    pet_breeds_dir = data_dir / "pet_breeds"
    metadata_dir = data_dir / "metadata"

    # Create sample breeds (matching the existing structure)
    sample_breeds = [
        "abyssinian",
        "american shorthair",
        "beagle",
        "boxer",
        "bulldog",
        "chihuahua",
        "corgi",
        "dachshund",
        "german shepherd",
        "golden retriever",
        "husky",
        "labrador",
        "maine coon",
        "mumbai cat",
        "persian cat",
        "pomeranian",
        "pug",
        "ragdoll cat",
        "rottwiler",
        "shiba inu",
        "siamese cat",
        "sphynx",
        "yorkshire terrier"
    ]

    print("📝 Creating sample dataset for testing...")

    # Create label map
    label_map = {i: breed for i, breed in enumerate(sample_breeds)}
    label_map_path = metadata_dir / "label_map.pkl"
    with open(label_map_path, "wb") as f:
        pickle.dump(label_map, f)

    # Create directories and placeholder files
    for breed in sample_breeds:
        breed_dir = pet_breeds_dir / breed
        breed_dir.mkdir(parents=True, exist_ok=True)

        # Create a placeholder file (in real scenario, you'd have actual images)
        placeholder_path = breed_dir / "placeholder.txt"
        with open(placeholder_path, "w") as f:
            f.write(f"Sample data for {breed} breed\n")
            f.write(f"This is a placeholder file for testing purposes.\n")
            f.write(f"In a real scenario, this would contain actual pet images.\n")

    print(f"✅ Sample dataset created!")
    print(f"   Breeds: {len(sample_breeds)}")
    print(f"   Note: This is a placeholder dataset for testing")
    print(f"   For real training, you need to provide actual pet images")

    return True


def download_from_url():
    """
    Alternative method to download dataset from a direct URL.
    This can be used if the dataset is hosted elsewhere.
    """
    try:
        # Example URL - replace with actual dataset URL
        url = "https://example.com/pet-breeds-dataset.zip"

        print(f"📥 Downloading dataset from: {url}")

        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
            urllib.request.urlretrieve(url, tmp_file.name)

            # Extract the zip file
            with zipfile.ZipFile(tmp_file.name, 'r') as zip_ref:
                zip_ref.extractall("data/")

        # Clean up
        os.unlink(tmp_file.name)

        print("✅ Dataset downloaded and extracted successfully!")
        return True

    except Exception as e:
        print(f"Error downloading from URL: {e}")
        return False


if __name__ == "__main__":
    # Try to fetch the main dataset first
    success = fetch_pet_breed_dataset()

    if not success:
        print("❌ Failed to fetch dataset. Please check your internet connection and dataset availability.")
        exit(1)

    print("🎉 Data fetching completed successfully!") 