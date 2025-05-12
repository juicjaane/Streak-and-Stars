import os
from PIL import Image

def convert_tiff_to_png(input_dir, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".tif", ".tiff")):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".png"
            output_path = os.path.join(output_dir, output_filename)

            try:
                with Image.open(input_path) as img:
                    img.save(output_path, format="PNG")
                    print(f"Converted: {filename} -> {output_filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

# Example usage
input_directory = "Annotated_Images"
output_directory = "C:\projects\Streak-and-Stars\png files"
convert_tiff_to_png(input_directory, output_directory)
