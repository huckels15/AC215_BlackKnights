from model import get_resnet
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import pandas as pd
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import datetime
import matplotlib.pyplot as plt

dt = datetime.datetime.today()
year = dt.year
month = dt.month
day = dt.day
hour = dt.hour
minute = dt.minute


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

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator()

def load_data():
    data = pd.read_csv("data/dvc_store_csvs_hmnist_28_28_RGB.csv")
    y = data['label']
    X = data.drop(columns= ['label'])

    X = X.values.reshape(-1, 28, 28, 3)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.1)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2)

    y_train = to_categorical(y_train, num_classes=7)
    y_val = to_categorical(y_val, num_classes=7)
    y_test = to_categorical(y_test, num_classes=7)

    X_train_resize = tf.image.resize(X_train, (224, 224))
    X_val_resize = tf.image.resize(X_val, (224, 224))
    X_test_resize = tf.image.resize(X_test, (224, 224))
    
    train_gen = train_datagen.flow(X_train_resize.numpy(), y_train, batch_size=64)
    val_gen = test_datagen.flow(X_val_resize.numpy(), y_val, batch_size=64)
    test_gen = test_datagen.flow(X_test_resize.numpy(), y_test, batch_size=64)
    return train_gen, val_gen, test_gen

if __name__ == "__main__":
    
    resnet = get_resnet()
    train_gen, val_gen, test_gen = load_data()

    resnet.compile(
        optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    history = resnet.fit(train_gen, epochs=100, validation_data=val_gen)
    model_name = f"trainedResnet_{year}{month:02d}{day:02d}_{hour:02d}{minute:02d}.h5"
    resnet.save("../models/" + model_name)
