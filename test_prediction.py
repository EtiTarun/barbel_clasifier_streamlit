# test_prediction.py
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

print("Starting test prediction script...")

model = tf.keras.models.load_model("model/barbell_model.h5")
print("Model loaded successfully!")

class_names = ['bench press', 'squat', 'deadlift', 'barbell biceps curl', 'shoulder press']


def predict_image(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = np.max(predictions)

    return predicted_class, confidence

if __name__ == "__main__":
    test_img_path = "dataset/test/bench press/000017.jpg"  # change as per your test image path
    pred_class, conf = predict_image(test_img_path)
    print(f"Prediction for '{test_img_path}': {pred_class} with confidence {conf:.2f}")

print("Test prediction completed!")
