import os
import numpy as np
from PIL import Image
import random

# Create output directory
os.makedirs(r"Data\Dataset_Raw_Augment_Noise\background", exist_ok=True)

# Image dimensions
width, height = 128, 128
total_images = 500  # 100 of each type
images_per_type = 250

# Background generation functions
def black_background():
    """Pure black image with random single-pixel activations"""
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # Add 1-5 random bright pixels
    for _ in range(random.randint(1, 5)):
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        img_array[y, x] = [255, 255, 255]  # White pixel
    return img_array

def cosmic_ray_background():
    """Black background with simulated cosmic ray streaks"""
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # Add 1-3 cosmic ray streaks
    for _ in range(random.randint(1, 3)):
        # Random start point
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        # Random length (5-15 pixels)
        length = random.randint(5, 15)
        # Random angle
        angle = random.uniform(0, 2 * np.pi)
        
        # Draw the streak
        for l in range(length):
            xx = int(x + l * np.cos(angle))
            yy = int(y + l * np.sin(angle))
            if 0 <= xx < width and 0 <= yy < height:
                # Make pixel bright (could add fading effect here)
                img_array[yy, xx] = [255, 255, 255]
    return img_array

# Generate images
for i in range(total_images):
    if i < images_per_type:
        img_array = black_background()
        img_type = "black_bg"
    else:
        img_array = cosmic_ray_background()
        img_type = "cosmic_ray_bg"
    
    # Save image
    img = Image.fromarray(img_array)
    img.save(fr"Data\Dataset_Raw_Augment_Noise\background\{img_type}_{i}.png")

print(f"Generated {total_images} background images in ./background_dataset/")