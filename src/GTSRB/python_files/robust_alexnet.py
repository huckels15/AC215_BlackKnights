import tensorflow as tf
import pandas as pd
import numpy as np
from art.estimators.classification import KerasClassifier
from art.attacks.evasion import ProjectedGradientDescent as PGD
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
tf.compat.v1.disable_eager_execution()

import tensorflow as tf
import pandas as pd
import numpy as np
from art.estimators.classification import KerasClassifier
from art.attacks.evasion import FastGradientMethod
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import os
import cv2

NUM_CLASSES = 43
IMG_HEIGHT, IMG_WIDTH = 32, 32

tf.compat.v1.disable_eager_execution()


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


if __name__ == "__main__":
    X_train, X_val, X_test, y_train, y_val, y_test = load_data("../data/Train")
    
    model_name = 'trainedAlexNet_20241118_1535'

    model = tf.keras.models.load_model(f"../models/{model_name}.h5")
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Accuracy on benign test examples: {test_accuracy * 100:.2f}%")

    min_pixel_value, max_pixel_value = 0.0, 255.0
    classifier = KerasClassifier(model=model, clip_values=(min_pixel_value, max_pixel_value), use_logits=False)

    attack = PGD(estimator=classifier, eps=0.2, eps_step=0.01, max_iter=40,targeted=False)

    X_test_adv = attack.generate(x=X_test)
    predictions_adv = classifier.predict(X_test_adv)
    accuracy_adv = np.sum(np.argmax(predictions_adv, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
    print(f"Accuracy on perturbed test examples pre adv training: {accuracy_adv * 100:.2f}%")

    x_train_adv = attack.generate(X_train)

    es = EarlyStopping(
        monitor="loss",
        min_delta=0.01,
        patience=5,
        verbose=0,
        mode="auto",
        baseline=None,
        restore_best_weights=True,
        start_from_epoch=0,
    )

    model.fit(
        x_train_adv,
        y_train,
        batch_size=32,
        epochs=20,
        callbacks=[es]
    )

    loss, acc = model.evaluate(X_test_adv, y_test)
    print(f"Accuracy on perturbed test examples post adv training: {acc * 100}%")
    model.save("../models/" + model_name + "_pgd_robust.h5")
