#need to pad to 128x128
from PIL import Image, ImageOps
import os
def pad(image_path,x,y, output_path):
    img = Image.open(image_path)
    w, h = img.size
    
    # Calculate padding
    pad_w = max(0,y - w)
    pad_h = max(0, x - h)
    
    # Apply padding (centered)
    padded_img = ImageOps.pad(
        img,
        size=(x, y),
        color='black',  # Black padding
        centering=(0.5, 0.5)  # Center the original image
    )
    
    padded_img.save(output_path)
    print(f"Padded image saved to: {output_path}")
image_dir = "Datasets/Raw_Images"
output_dir="Datasets/Padded_Raw"  # Directory containing images
for img_name in os.listdir(image_dir):

    input_path = os.path.join(image_dir, img_name)
    output_path = os.path.join(output_dir, f"{img_name}")
    pad(input_path,4500,4500, output_path)

