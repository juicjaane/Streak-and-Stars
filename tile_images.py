import os
import pandas as pd
import numpy as np
from PIL import Image

# Parameters
TILE_SIZE = 128
STRIDE = 128
INPUT_IMAGE_DIR = "Processed"
OUTPUT_IMAGE_DIR = f"TiledImages_{TILE_SIZE}"
OUTPUT_CSV_PATH = f"tiled_annotations_{TILE_SIZE}.csv"

os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)

# Load original annotations
df = pd.read_csv("centroids.csv")

# New annotations will go here
tiled_annotations = []

# Get list of unique images
image_names = df['image'].unique()

for image_name in image_names:
    image_path = os.path.join(INPUT_IMAGE_DIR, os.path.splitext(image_name)[0] + "_binary.tiff")
    original_img = Image.open(image_path).convert("RGB")
    img_w, img_h = original_img.size

    # Get all boxes for this image
    records = df[df['image'] == image_name]

    for top in range(0, img_h, STRIDE):
        for left in range(0, img_w, STRIDE):
            bottom = min(top + TILE_SIZE, img_h)
            right = min(left + TILE_SIZE, img_w)

            # Crop tile
            tile = original_img.crop((left, top, right, bottom))
            tile_filename = f"{os.path.splitext(image_name)[0]}_{top}_{left}.tiff"
            tile.save(os.path.join(OUTPUT_IMAGE_DIR, tile_filename))

            # Check if any boxes are in this tile
            for _, row in records.iterrows():
                x1 = row['bbox_x']
                y1 = row['bbox_y']
                x2 = x1 + row['bbox_width']
                y2 = y1 + row['bbox_height']

                # Check if box intersects tile
                if x2 <= left or x1 >= right or y2 <= top or y1 >= bottom:
                    continue  # skip box

                # Clip box to tile and adjust coordinates
                new_x1 = max(x1, left) - left
                new_y1 = max(y1, top) - top
                new_x2 = min(x2, right) - left
                new_y2 = min(y2, bottom) - top

                new_w = new_x2 - new_x1
                new_h = new_y2 - new_y1

                if new_w > 1 and new_h > 1:  # discard tiny boxes
                    tiled_annotations.append({
                        'image': tile_filename,
                        'bbox_x': new_x1,
                        'bbox_y': new_y1,
                        'bbox_width': new_w,
                        'bbox_height': new_h,
                        'object_type': row['object_type']
                    })

# Save new annotations
pd.DataFrame(tiled_annotations).to_csv(OUTPUT_CSV_PATH, index=False)
print(f"✅ Done. Tiled images saved to {OUTPUT_IMAGE_DIR}, annotations to {OUTPUT_CSV_PATH}")
