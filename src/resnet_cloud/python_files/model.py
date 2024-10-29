import tensorflow as tf
from tensorflow.keras.applications import ResNet101
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Input

def get_resnet():
    resnet = ResNet101(weights='imagenet', include_top = False)
    resnet.trainable = False
    inputs = Input(shape=(224, 224, 3))
    x = resnet(inputs)
    x = Flatten()(x)
    x = Dense(128, activation = 'relu')(x)
    output = Dense(7, activation = 'softmax')(x)

    model = Model(inputs, output)
    model.summary()

    return model
    