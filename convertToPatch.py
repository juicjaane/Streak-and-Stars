import os
import numpy as np
from PIL import Image
import tifffile  # For TIFF handling (install with `pip install tifffile`)

def split_image_into_patches(image_path, patch_size=64, output_dir="patches"):
    """Split a single image into patches and save them."""
    # Load image (support both TIFF and other formats)
    if image_path.lower().endswith('.tiff') or image_path.lower().endswith('.tif'):
        image = tifffile.imread(image_path)
    else:
        image = np.array(Image.open(image_path))
    
    # Pad the image to make dimensions divisible by patch_size
    height, width = image.shape[:2]
    pad_height = (patch_size - height % patch_size) % patch_size
    pad_width  = (patch_size - width % patch_size) % patch_size
    
    padded_image = np.pad(
        image,
        ((0, pad_height), (0, pad_width)),
        mode="constant",  # Options: 'constant', 'reflect', 'edge'
        constant_values=0  # Fill value (adjust if needed)
    )
    
    # Create subdirectory for patches of this image
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    image_output_dir = "patches"  # Base output directory
    os.makedirs(image_output_dir, exist_ok=True)
   
    
    # Extract and save patches
    patch_count = 0
    for y in range(0, padded_image.shape[0], patch_size):
        for x in range(0, padded_image.shape[1], patch_size):
            patch = padded_image[y:y+patch_size, x:x+patch_size]
            patch_filename = os.path.join(image_output_dir, f"patch_{patch_count}.tiff")
            tifffile.imwrite(patch_filename, patch)  # Or use PIL for other formats
            patch_count += 1
    
    print(f"Saved {patch_count} patches for {image_name} in {image_output_dir}.")

def process_directory(input_dir, patch_size=64, output_dir="patches"):
    """Process all images in a directory into patches."""
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.tiff', '.tif', '.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_dir, filename)
            split_image_into_patches(image_path, patch_size, output_dir)

# Usage
input_directory = r"Datasets\Raw_Images"  # Replace with your directory
process_directory(input_directory, patch_size=64, output_dir="patches")