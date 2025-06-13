# train_model.py
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np

print("🔧 Starting training script...")

# Paths
train_dir = "dataset/train"
val_dir = "dataset/val"
model_dir = "model"
os.makedirs(model_dir, exist_ok=True)

# Image data generators
print(f"📂 Loading training data from: {train_dir}")
train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True, rotation_range=10, zoom_range=0.1)
train_data = train_datagen.flow_from_directory(train_dir, target_size=(128, 128), batch_size=32, class_mode='categorical')

print(f"📂 Loading validation data from: {val_dir}")
val_datagen = ImageDataGenerator(rescale=1./255)
val_data = val_datagen.flow_from_directory(val_dir, target_size=(128, 128), batch_size=32, class_mode='categorical')

# Extract class names
class_names = list(train_data.class_indices.keys())
num_classes = len(class_names)
print(f"✅ Detected class labels: {class_names}")

# CNN Model
print("🧠 Building custom CNN model...")
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(2, 2),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Early stopping
early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Training
print("🚀 Starting training...")
history = model.fit(
    train_data,
    epochs=25,
    validation_data=val_data,
    callbacks=[early_stop]
)

# Save model
model_path = os.path.join(model_dir, "barbell_model.h5")
model.save(model_path)
print(f"✅ Custom model trained and saved at: {model_path}")

# Save training history
print("🔍 History keys:", history.history.keys())
print("📁 Model dir exists:", os.path.exists(model_dir))
history_path = os.path.join(model_dir, "training_history.npy")
np.save(history_path, history.history)
print(f"📈 Training history saved at: {history_path}")

print("🎉 Training script completed successfully!")


# Save class names to JSON
import json

class_names_path = os.path.join(model_dir, "class_names.json")
with open(class_names_path, "w") as f:
    json.dump(class_names, f)
print(f"📄 Class names saved at: {class_names_path}")

print("🎉 Training script completed successfully!")