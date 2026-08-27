from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import os

# -----------------------------
# LOAD MODEL
# -----------------------------
model = load_model("model/fmodel.keras")

print("Model loaded successfully!")
print("Input shape:", model.input_shape)
print("Output shape:", model.output_shape)

# -----------------------------
# TEST IMAGE
# -----------------------------
image_path = "test_image.jpg"

if not os.path.exists(image_path):
    print("ERROR: test_image.jpg not found!")
    exit()

print("Test image found:", image_path)

# -----------------------------
# LOAD & PREPROCESS IMAGE
# -----------------------------
img = load_img(
    image_path,
    target_size=(224, 224)
)

img_array = img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

print("Image shape:", img_array.shape)

# -----------------------------
# PREDICTION
# -----------------------------
prediction = model.predict(img_array)

print("Raw prediction:", prediction)

predicted_class = np.argmax(prediction[0])
confidence = np.max(prediction[0]) * 100

print("Predicted class:", predicted_class)
print("Confidence:", confidence, "%")