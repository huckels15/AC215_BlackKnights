import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from train_resnet import test_datagen, train_datagen, load_data


if __name__ == "__main__":

    model_name = '../models/trainedResnet_20241016_2112.h5'
    model = load_model(model_name)
    train_gen, val_gen, test_gen = load_data()
    test_loss, test_accuracy = model.evaluate(test_gen)
    print(f"The test accuracy for ResNet is: {test_accuracy}.")

