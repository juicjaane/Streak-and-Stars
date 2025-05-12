import pandas as pd

# Load the CSV
df = pd.read_csv("..\eccentricity_data.csv")  # replace with your actual filename

# Compute centroid coordinates
df['centroid_x'] = df['bbox_x'] + df['bbox_width'] / 2
df['centroid_y'] = df['bbox_y'] + df['bbox_height'] / 2

# Save to a new CSV (optional)
df.to_csv("entroids.csv", index=False)

# Print the updated DataFrame (optional)
print(df.head())
