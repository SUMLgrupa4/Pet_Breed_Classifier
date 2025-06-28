#!/usr/bin/env python3
"""
Debug script to check data structure and image validation
"""

import os
from PIL import Image
from pathlib import Path

def debug_data_structure():
    """Debug the data structure and image validation"""
    
    BASE_DIR = Path(__file__).parent
    raw_data_path = BASE_DIR / 'data' / 'pet_breeds'
    
    print("🔍 Debugging Data Structure")
    print("=" * 50)
    
    if not raw_data_path.exists():
        print(f"❌ Data directory not found: {raw_data_path}")
        return
    
    print(f"✅ Data directory found: {raw_data_path}")
    
    # Check each breed directory
    total_images = 0
    valid_images = 0
    invalid_images = 0
    
    for breed_dir in raw_data_path.iterdir():
        if not breed_dir.is_dir():
            continue
            
        breed_name = breed_dir.name
        print(f"\n🐕 Checking {breed_name}:")
        
        breed_images = 0
        breed_valid = 0
        breed_invalid = 0
        
        # Check all image files
        for image_file in breed_dir.glob("*"):
            if not image_file.is_file():
                continue
                
            if not image_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                continue
                
            breed_images += 1
            total_images += 1
            
            try:
                with Image.open(image_file) as img:
                    # Check image size
                    if img.size[0] > 50 and img.size[1] > 50:
                        breed_valid += 1
                        valid_images += 1
                        print(f"   ✅ {image_file.name}: {img.size} ({img.mode})")
                    else:
                        breed_invalid += 1
                        invalid_images += 1
                        print(f"   ❌ {image_file.name}: Too small {img.size}")
                        
            except Exception as e:
                breed_invalid += 1
                invalid_images += 1
                print(f"   ❌ {image_file.name}: Error - {e}")
        
        print(f"   📊 {breed_name}: {breed_valid}/{breed_images} valid images")
    
    print(f"\n📈 Summary:")
    print(f"   Total images found: {total_images}")
    print(f"   Valid images: {valid_images}")
    print(f"   Invalid images: {invalid_images}")
    print(f"   Success rate: {valid_images/total_images*100:.1f}%" if total_images > 0 else "No images found")

if __name__ == "__main__":
    debug_data_structure() 