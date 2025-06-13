# evaluate_model.py
import numpy as np
import matplotlib.pyplot as plt

history = np.load("model/training_history.npy", allow_pickle=True).item()

print("Final Training Accuracy:", history['accuracy'][-1])
print("Final Validation Accuracy:", history['val_accuracy'][-1])

history = np.load("model/training_history.npy", allow_pickle=True).item()
print("Epochs trained:", len(history['accuracy']))


plt.plot(history['accuracy'], label='Train Accuracy')
plt.plot(history['val_accuracy'], label='Validation Accuracy')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Training and Validation Accuracy")
plt.legend()
plt.grid(True)
plt.show()
