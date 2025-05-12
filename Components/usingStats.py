import cv2
import numpy as np
import os
import pandas as pd
from skimage.measure import regionprops
import glob

# Create directories to store stars and streaks if they don't exist
os.makedirs('stars-images', exist_ok=True)
os.makedirs('streaks-images', exist_ok=True)

# Folder containing TIFF images
image_folder = r"Datasets\Raw_Images"
image_files = glob.glob(os.path.join(image_folder, "*.tiff"))

# Parameters
area_threshold = 50
eccentricity_threshold = 0.85
min_dist = 10  # minimum centroid distance to avoid duplicate objects

# Initialize final CSV containers
all_eccentricity_data = []
all_image_stats = []

# Iterate through images
for image_path in image_files:
    image_name = os.path.basename(image_path)
    print(f"\nProcessing: {image_name}")

    # Read 16-bit image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Convert 16-bit to 8-bit
    img_8bit = cv2.convertScaleAbs(img, alpha=(255.0 / 65535.0))

    # Apply CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    blurred = cv2.GaussianBlur(img_8bit, (5, 5), 0)
    img_clahe = clahe.apply(blurred)

    # Binary threshold
    _, binary = cv2.threshold(img_clahe, 10, 255, cv2.THRESH_BINARY)

    # Label connected components
    num_labels, labels = cv2.connectedComponents(binary)

    # Get regions
    regions = regionprops(labels)

    star_objects = []
    streak_objects = []
    filtered_regions = []

    for region in regions:
        if region.area < area_threshold:
            continue

        centroid = region.centroid

        # Filter nearby duplicates
        if any(np.linalg.norm(np.array(centroid) - np.array(r.centroid)) < min_dist for r in filtered_regions):
            continue

        filtered_regions.append(region)
        eccentricity = region.eccentricity
        bbox = region.bbox
        x, y = int(centroid[0]), int(centroid[1])

        if eccentricity < eccentricity_threshold:
            obj_type = "star"
            star_objects.append(region)
            save_path = f"stars-images/star_{image_name[:-5]}_{x}_{y}.png"
        else:
            obj_type = "streak"
            streak_objects.append(region)
            save_path = f"streaks-images/streak_{image_name[:-5]}_{x}_{y}.png"

        # Crop and save the region
        cropped = binary[bbox[0]:bbox[2], bbox[1]:bbox[3]]
        cv2.imwrite(save_path, cropped)

        # Append eccentricity data
        all_eccentricity_data.append({
            'image': image_name,
            'object_type': obj_type,
            'object_name': os.path.basename(save_path),
            'eccentricity': eccentricity
        })

    # Append per-image stats
    all_image_stats.append({
        'image_name': image_name,
        'no_of_stars': len(star_objects),
        'no_of_streaks': len(streak_objects)
    })

# Save all CSVs at once
pd.DataFrame(all_eccentricity_data).to_csv('eccentricity_data.csv', index=False)
pd.DataFrame(all_image_stats).to_csv('image_stats.csv', index=False)

print("\n✅ Processing complete. CSVs and images saved.")
