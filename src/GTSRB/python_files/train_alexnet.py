import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import pandas as pd
import numpy as np
import cv2
import os
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import datetime
import matplotlib.pyplot as plt
import wandb
from alexnet import create_alexnet
from wandb.integration.keras import WandbCallback
import datetime

dt = datetime.datetime.today()
year = dt.year
month = dt.month
day = dt.day
hour = dt.hour
minute = dt.minute

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

es = EarlyStopping(
    monitor="val_loss",
    min_delta=0.01,
    patience=10,
    verbose=0,
    mode="auto",
    baseline=None,
    restore_best_weights=True,
    start_from_epoch=0,
)

if __name__ == "__main__":

    model_name = f"trainedAlexNet_{year}{month:02d}{day:02d}_{hour:02d}{minute:02d}.h5"
    
    path = "../data/Train"

    IMG_HEIGHT, IMG_WIDTH = 32, 32
    NUM_CLASSES = 43

    X_train, X_val, X_test, y_train, y_val, y_test = load_data(path)

    model = create_alexnet()

    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])


    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=100,
        batch_size=32,
        callbacks=[es]
    )

    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"The test accuracy is {test_acc * 100}.")

    model.save("../models/" + model_name)
