import os
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

train_data_path = os.path.join(BASE_DIR, "data", "splits", "train_data.csv")
label_map_path = os.path.join(BASE_DIR, "data", "metadata", "label_map.pkl")

print("BASE_DIR:", BASE_DIR)
print("Train data path:", train_data_path)
print("Label map will be saved to:", label_map_path)

os.makedirs(os.path.dirname(label_map_path), exist_ok=True)

train_df = pd.read_csv(train_data_path)

label_map = {}
for _, row in train_df.iterrows():
    label = int(row['label'])
    path = row['image']
    class_name = os.path.basename(os.path.dirname(path))
    label_map[label] = class_name

label_map = dict(sorted(label_map.items()))

with open(label_map_path, "wb") as f:
    pickle.dump(label_map, f)

print(f"Saved label_map to: {label_map_path}")
for k, v in label_map.items():
    print(f"{k}: {v}")
