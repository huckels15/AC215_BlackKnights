import os
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import array_to_img

(_, _), (x_test, y_test) = mnist.load_data()

x_test = (x_test * 255).astype(np.uint8)
y_test = np.argmax(to_categorical(y_test, num_classes=10), axis=1)

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

for i in range(10):
    class_dir = os.path.join(output_dir, str(i))
    os.makedirs(class_dir, exist_ok=True)

class_counters = {i: 0 for i in range(10)}

for i, (image, label) in enumerate(zip(x_test, y_test)):
    if class_counters[label] < 50:  # Save up to 50 images per class
        class_dir = os.path.join(output_dir, str(label))
        image_path = os.path.join(class_dir, f"{label}_{class_counters[label]}.png")
        img = array_to_img(image.reshape(28, 28, 1), scale=False)
        img.save(image_path)
        class_counters[label] += 1

    if all(count == 50 for count in class_counters.values()):
        break

print(f"MNIST test data saved to: {output_dir}")
