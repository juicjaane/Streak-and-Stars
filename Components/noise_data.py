import os
import numpy as np
from PIL import Image, ImageEnhance

# Create output directory
os.makedirs("Data/Dataset_Raw_Augment_Noise/noise", exist_ok=True)

# Image dimensions
width, height = 128, 128
total_images = 600
images_per_type = 100
# Noise/pattern generation functions
def uniform_noise():
    noise = np.random.randint(0, 256, (height, width, 1), dtype=np.uint8)
    return np.concatenate([noise]*3, axis=-1)

def gaussian_noise():
    noise = np.random.normal(128, 50, (height, width, 1)).clip(0, 255).astype(np.uint8)
    return np.concatenate([noise]*3, axis=-1)

def salt_pepper_noise():
    noise = np.random.choice([0, 255], size=(height, width, 1), p=[0.95, 0.05]).astype(np.uint8)
    return np.concatenate([noise]*3, axis=-1)




# Generate images
for i in range(total_images):
    # Start with black background
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    if i < images_per_type*1:
        img_array = uniform_noise()
        img_type = "uniform"
    elif i < images_per_type*2:
        img_array = gaussian_noise()
        img_type = "gaussian"
    else:
        img_array = salt_pepper_noise()
        img_type = "salt_pepper"
    

    # Ensure black background for non-pattern areas
    if img_type in ["gradient", "grid"]:
        threshold = 50
        mask = np.mean(img_array, axis=-1) < threshold
        img_array[mask] = 0

    # Save image
    img = Image.fromarray(img_array)
    img.save(f"Data/Dataset_Raw_Augment_Noise/noise/{img_type}_{i}.png")

print(f"Generated {total_images} images in ./noise_dataset/")