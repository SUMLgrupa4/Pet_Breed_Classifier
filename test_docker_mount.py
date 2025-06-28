#!/usr/bin/env python3
"""
Test script to check Docker volume mounting and image accessibility
"""

import os
from pathlib import Path

def test_docker_mount():
    """Test if Docker volume mounting is working"""
    
    print("🐳 Testing Docker Volume Mount")
    print("=" * 40)
    
    # Check if we're in Docker
    in_docker = os.path.exists('/.dockerenv')
    print(f"In Docker container: {in_docker}")
    
    # Check data directory
    data_dir = Path('/app/data') if in_docker else Path('./data')
    print(f"Data directory: {data_dir}")
    print(f"Data directory exists: {data_dir.exists()}")
    
    if data_dir.exists():
        print(f"Data directory contents: {list(data_dir.iterdir())}")
        
        # Check pet_breeds directory
        pet_breeds_dir = data_dir / 'pet_breeds'
        print(f"Pet breeds directory: {pet_breeds_dir}")
        print(f"Pet breeds directory exists: {pet_breeds_dir.exists()}")
        
        if pet_breeds_dir.exists():
            breeds = list(pet_breeds_dir.iterdir())
            print(f"Number of breed directories: {len(breeds)}")
            
            # Check first few breeds
            for breed_dir in breeds[:3]:
                if breed_dir.is_dir():
                    images = list(breed_dir.glob("*.jpg")) + list(breed_dir.glob("*.jpeg")) + list(breed_dir.glob("*.png"))
                    print(f"  {breed_dir.name}: {len(images)} images")
                    
                    # Check first image
                    if images:
                        first_image = images[0]
                        print(f"    First image: {first_image}")
                        print(f"    Image exists: {first_image.exists()}")
                        print(f"    Image size: {first_image.stat().st_size} bytes")
                        print(f"    Image readable: {os.access(first_image, os.R_OK)}")
    else:
        print("❌ Data directory not found!")
    
    # Check current working directory
    print(f"\nCurrent working directory: {os.getcwd()}")
    print(f"Current directory contents: {list(Path('.').iterdir())}")

if __name__ == "__main__":
    test_docker_mount() 