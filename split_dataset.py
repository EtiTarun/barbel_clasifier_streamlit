# split_dataset.py
import os
import shutil
import random

# Clean existing train/val/test folders
for split in ['train', 'val', 'test']:
    split_path = os.path.join("dataset", split)
    if os.path.exists(split_path):
        shutil.rmtree(split_path)

source_base = "dataset/all_images"
dest_base = "dataset"

split_ratios = {'train': 0.6, 'val': 0.2, 'test': 0.2}
classes = os.listdir(source_base)

for split in split_ratios:
    for cls in classes:
        os.makedirs(os.path.join(dest_base, split, cls), exist_ok=True)

for cls in classes:
    src_folder = os.path.join(source_base, cls)
    images = os.listdir(src_folder)
    random.shuffle(images)

    total = len(images)
    train_end = int(total * split_ratios['train'])
    val_end = train_end + int(total * split_ratios['val'])

    splits = {
        'train': images[:train_end],
        'val': images[train_end:val_end],
        'test': images[val_end:]
    }

    for split, files in splits.items():
        for img_file in files:
            shutil.copy2(
                os.path.join(src_folder, img_file),
                os.path.join(dest_base, split, cls, img_file)
            )

print("✅ Dataset successfully split into train, val, and test.")
