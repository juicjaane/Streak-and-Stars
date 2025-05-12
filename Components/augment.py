import os
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Define pure PyTorch augmentations
augments = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(degrees=15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
])

# Define Albumentations augmentations
albumentations_aug = A.Compose([
    A.RandomShadow(shadow_roi=(0, 0, 1, 1), p=0.3),
    A.ElasticTransform(alpha=1, sigma=50, p=0.5),
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
    A.GaussianBlur(blur_limit=(3, 7)),
])


# Paths
original_dir = r'..\streaks-images'  # Original images
augmented_dir = r'..\Data\Dataset_Thresh_Augment\streaks'   # Where to save new images
os.makedirs(augmented_dir, exist_ok=True)

for img_name in os.listdir(original_dir):
    img_path = os.path.join(original_dir, img_name)
    img = Image.open(img_path)
    
    # Generate N augmented versions per image
    for i in range(15):
        # Apply PyTorch transforms
        augmented_img = augments(img)
        
        # Convert to numpy array for Albumentations
        img_np = np.array(augmented_img)
        
        # Apply Albumentations transforms
        augmented_np = albumentations_aug(image=img_np)['image']
        
        # Convert back to PIL Image
        final_img = Image.fromarray(augmented_np)
        
        # Save the image
        final_img.save(os.path.join(augmented_dir, f'aug_{i}_{img_name}'))