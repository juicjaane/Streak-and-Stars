#need to pad to 128x128
from PIL import Image, ImageOps
import os
def pad_to_128x128_pil(image_path, output_path):
    img = Image.open(image_path)
    w, h = img.size
    
    # Calculate padding
    pad_w = max(0, 128 - w)
    pad_h = max(0, 128 - h)
    
    # Apply padding (centered)
    padded_img = ImageOps.pad(
        img,
        size=(128, 128),
        color='black',  # Black padding
        centering=(0.5, 0.5)  # Center the original image
    )
    
    padded_img.save(output_path)
    print(f"Padded image saved to: {output_path}")
image_dir = r"..\stars-images"  # Directory containing images
for img_name in os.listdir(image_dir):

    input_path = os.path.join(image_dir, img_name)
    output_path = os.path.join(image_dir, f"{img_name}")
    pad_to_128x128_pil(input_path, output_path)

