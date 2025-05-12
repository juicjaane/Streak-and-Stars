# 🌠 Streaks and Star Detection – Digantara
An image processing and machine learning pipeline to detect and classify **stars** and **streaks** from synthetic astronomical TIFF images.

**Internship Assessment – AI/ML**
- **Author**: Janeshvar Sivakumar
- **Organization**: Digantara
- **Tech**: Python, OpenCV, NumPy, Scikit-learn, PyTorch/TensorFlow

---

## 📌 Overview

The objective is to classify **stars (point sources)** and **streaks (elongated trails)** from unlabelled 16-bit synthetic TIFF images, using image processing techniques and later a supervised ML/DL model for generalizability.

---

## 🧠 Key Ideas

- **Initial dataset is unlabelled** → we generate labels using image processing.
- **Image Preprocessing**: Convert 16-bit TIFF → 8-bit, bilateral filtering for noise, CLAHE for contrast.
- **Segmentation**: Morphological ops, adaptive thresholding, eccentricity-based classification.
- **Label Generation**: Classify connected components by **eccentricity** to create synthetic labels.
- **Model Training**: Use labels to train ML/DL model with augmentations and fine-tuning.
- **Deployment Vision**: Optimized for edge deployment → low-latency inference.

---

## 🧪 Image Processing Pipeline

### ✅ Preprocessing
- Convert 16-bit TIFF → 8-bit for faster processing.
- Apply **Bilateral Filter** (Gaussian-like noise removal).
- Apply **CLAHE** (Contrast Limited Adaptive Histogram Equalization) for local contrast.

### ✅ Feature Extraction & Classification
- Adaptive thresholding using **median intensity**.
- **Morphological Dilation** for streak gap filling.
- **Connected Components** → calculate **eccentricity**:
  - `e < 0.9`: Star
  - `e >= 0.9`: Streak

### ✅ Label Generation
- Filter by:
  - Minimum area
  - Minimum inter-object distance
- Assign labels for model training.

---

## 🤖 Model Training & Deep Learning

### ✔️ Architecture
- Transfer learning using **Faster R-CNN with ResNet-18**
- Augmented synthetic dataset used for fine-tuning.

### ✔️ Strategies for Low-Data Regime
- **Transfer Learning**
- **Data Augmentation**: Rotation, flipping, synthetic streaks
- (Explored but not fully implemented) **Few-shot/Zero-shot learning**

---

## 📊 Evaluation

### Metrics
- Accuracy, Precision, Recall
- Confusion Matrix (False Positives / Negatives)
- Intersection-over-Union (IoU) for streak bounding

### Common Errors
- False positives: background noise detected as blobs
- Multiple blobs along one streak
- Misclassified faint stars/streaks

---

## 🧭 Future Work

| Technique | Purpose |
|----------|---------|
| 🧲 Matched Filters (Gabor kernels) | Enhance streak features |
| ➖ Hough Transforms | Detect straight line segments (streaks) |
| 🪞 Image Layer Separation | Process bright/dark/faint separately |
| 🧠 Deep Hough Transform CNNs | Improve generalization on real sky images |

---

## 🖼 Sample Results

| Input Image | After Preprocessing | Final Classification |
|-------------|---------------------|-----------------------|
| ![](images/input.png) | ![](images/preprocessed.png) | ![](images/result.png) |

<sup>*Visualizations will be added from `.ipynb` output*</sup>

---

## 📂 Repository Structure

```bash
StreakStarDetection/
├── data/                 # Raw TIFF images
├── notebooks/            # Jupyter notebooks for processing and training
├── models/               # Trained model files (if available)
├── src/
│   ├── preprocessing.py  # Image enhancement & filtering
│   ├── segment.py        # Thresholding & morphological ops
│   ├── features.py       # Eccentricity calculation
│   ├── train_model.py    # Model training
│   └── evaluate.py       # Evaluation & metrics
├── images/               # Visual output samples
├── README.md
└── requirements.txt
