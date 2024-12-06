
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout
from tensorflow.keras.regularizers import l2

def create_alexnet():
    alexnet = Sequential()

    alexnet.add(Conv2D(64, (3, 3), input_shape=(32, 32, 3), padding='same', kernel_regularizer=l2(0.0005)))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    alexnet.add(Conv2D(128, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    alexnet.add(Conv2D(256, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    alexnet.add(Conv2D(512, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))

    alexnet.add(Conv2D(512, (3, 3), padding='same'))
    alexnet.add(Activation('relu'))
    alexnet.add(MaxPooling2D(pool_size=(2, 2)))

    alexnet.add(Flatten())
    alexnet.add(Dense(512, activation='relu'))
    alexnet.add(Dropout(0.5))

    alexnet.add(Dense(512, activation='relu'))
    alexnet.add(Dropout(0.5))

    alexnet.add(Dense(43, activation='softmax'))

    return alexnet