import os
import random
from PIL import Image
import matplotlib.pyplot as plt

def show_random_grayscale_image_grid(directory, grid_size=(10, 10), image_size=(64, 64)):
    image_files = [f for f in os.listdir(directory) if f.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff"))]
    random.shuffle(image_files)  # Shuffle the image list
    image_files = image_files[:grid_size[0] * grid_size[1]]  # Take the first 100 after shuffling

    fig, axes = plt.subplots(grid_size[0], grid_size[1], figsize=(10, 10))
    plt.subplots_adjust(wspace=0.01, hspace=0.01)  # Minimize gaps

    for ax, image_file in zip(axes.flatten(), image_files):
        img_path = os.path.join(directory, image_file)
        img = Image.open(img_path).convert("L").resize(image_size)
        ax.imshow(img, cmap="gray", vmin=0, vmax=255)
        ax.axis('off')

    for ax in axes.flatten()[len(image_files):]:
        ax.axis('off')

    plt.show()

# Example usage
directory = r"C:\projects\Streak-and-Stars\Data\Dataset_Raw_Augment_Noise\background"
show_random_grayscale_image_grid(directory)
