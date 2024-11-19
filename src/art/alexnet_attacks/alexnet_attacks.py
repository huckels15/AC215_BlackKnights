import tensorflow as tf
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent as PGD, DeepFool, SquareAttack as Square
from art.estimators.classification import KerasClassifier
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
tf.compat.v1.disable_eager_execution()
import pandas as pd
from tensorflow.keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import cv2
import json


IMG_HEIGHT, IMG_WIDTH = 32, 32
NUM_CLASSES = 43


def load_data(dataset_path):
    images, labels = [], []
    for class_id in range(NUM_CLASSES):
        class_path = os.path.join(dataset_path, str(class_id))
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))  # Resize image
            images.append(img)
            labels.append(class_id)

    images = np.array(images)
    labels = np.array(labels)

    images = images / 255.0

    labels = to_categorical(labels, NUM_CLASSES)

    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    return X_train, X_val, X_test, y_train, y_val, y_test


def plot_samples(num_samples, x_test, x_test_adv, y_test, predictions_adv):
    class_map = {
        0: 'Speed limit (20km/h)',
        1: 'Speed limit (30km/h)',
        2: 'Speed limit (50km/h)',
        3: 'Speed limit (60km/h)',
        4: 'Speed limit (70km/h)',
        5: 'Speed limit (80km/h)',
        6: 'End of speed limit (80km/h)',
        7: 'Speed limit (100km/h)',
        8: 'Speed limit (120km/h)',
        9: 'No passing',
        10: 'No passing for vehicles over 3.5 metric tons',
        11: 'Right-of-way at the next intersection',
        12: 'Priority road',
        13: 'Yield',
        14: 'Stop',
        15: 'No vehicles',
        16: 'Vehicles over 3.5 metric tons prohibited',
        17: 'No entry',
        18: 'General caution',
        19: 'Dangerous curve to the left',
        20: 'Dangerous curve to the right',
        21: 'Double curve',
        22: 'Bumpy road',
        23: 'Slippery road',
        24: 'Road narrows on the right',
        25: 'Road work',
        26: 'Traffic signals',
        27: 'Pedestrians',
        28: 'Children crossing',
        29: 'Bicycles crossing',
        30: 'Beware of ice/snow',
        31: 'Wild animals crossing',
        32: 'End of all speed and passing limits',
        33: 'Turn right ahead',
        34: 'Turn left ahead',
        35: 'Ahead only',
        36: 'Go straight or right',
        37: 'Go straight or left',
        38: 'Keep right',
        39: 'Keep left',
        40: 'Roundabout mandatory',
        41: 'End of no passing',
        42: 'End of no passing by vehicles over 3.5 metric tons'
    }

    for i in range(num_samples):
        true_label = class_map[y_test[i]]  # Use class indices directly
        adv_pred_label = class_map[np.argmax(predictions_adv[i])]  # Predicted class from model

        fig, ax = plt.subplots(1, 2, figsize=(10, 5))

        ax[0].imshow(x_test[i].astype(np.uint8))
        ax[0].set_title(f"Original\nTrue: {true_label}", fontsize=12, color="green")
        ax[0].axis('off')

        ax[1].imshow(x_test_adv[i].astype(np.uint8))
        ax[1].set_title(f"Adversarial\nTrue: {true_label}\nPred: {adv_pred_label}", fontsize=12, color="red")
        ax[1].axis('off')

        fig.suptitle(f"Example {i + 1}", fontsize=14, fontweight="bold")
        plt.savefig(f"figures/example_{i + 1}_original_vs_adversarial.png")
        path = f"figures/example_{i + 1}_original_vs_adversarial.png"
        return path
    
parser = argparse.ArgumentParser()
parser.add_argument(
    "--fgsm", 
    action="store_true", 
    help="Run FGSM attack"
)
parser.add_argument(
    "--pgd", 
    action="store_true", 
    help="Run PGD attack"
)
parser.add_argument(
    "--deepfool", 
    action="store_true", 
    help="Run DeepFool attack"
)
parser.add_argument(
    "--square", 
    action="store_true", 
    help="Run Square attack"
)

args = parser.parse_args()

path = "../../GTSRB/data/Train"

X_train, X_val, X_test, y_train, y_val, y_test = load_data(path)
custom_objects = {"Adam": Adam}

model = tf.keras.models.load_model("../models/trainedAlexNet_20241118_1535.h5", custom_objects=custom_objects, compile=False)
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

min_pixel_value, max_pixel_value = 0.0, 1.0
classifier = KerasClassifier(model=model, clip_values=(min_pixel_value, max_pixel_value), use_logits=False)

predictions = classifier.predict(X_test)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print("Accuracy on benign test examples: {:.2f}%".format(accuracy * 100))

if args.fgsm:
    print("Running FGSM attack...")
    attack = FastGradientMethod(estimator=classifier, eps=0.2)
elif args.pgd:
    print("Running PGD attack...")
    attack = PGD(estimator=classifier, eps=0.2, eps_step=0.01, max_iter=40)
elif args.deepfool:
    print("Running DeepFool attack...")
    attack = DeepFool(classifier=classifier, max_iter=50)
elif args.square:
    print("Running Square attack...")
    attack = Square(estimator=classifier, eps=0.2, max_iter=100)

x_test_adv = attack.generate(x=X_test)

predictions_adv = classifier.predict(x_test_adv)
accuracy_adv = np.sum(np.argmax(predictions_adv, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print("Accuracy on adversarial test examples: {:.2f}%".format(accuracy_adv * 100))

plot_samples(1, X_test, x_test_adv, y_test, predictions_adv)

results = {
    "reg_acc": (accuracy) * 100,
    "adv_acc": (accuracy_adv) * 100,
    "figure": path
}

print(json.dumps(results))