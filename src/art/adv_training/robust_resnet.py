import tensorflow as tf
import pandas as pd
import numpy as np
from art.estimators.classification import KerasClassifier
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent as PGD, DeepFool, SquareAttack as Square
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

tf.compat.v1.disable_eager_execution()


def load_data():
    data = pd.read_csv("../data/dvc_store_csvs_hmnist_28_28_RGB.csv")
    y = data['label']
    X = data.drop(columns=['label'])

    X = X.values.reshape(-1, 28, 28, 3)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    y_train = to_categorical(y_train, num_classes=7)
    y_val = to_categorical(y_val, num_classes=7)
    y_test = to_categorical(y_test, num_classes=7)

    with tf.compat.v1.Session() as sess:
        X_train = sess.run(tf.image.resize(X_train, (224, 224)))
        X_val = sess.run(tf.image.resize(X_val, (224, 224)))
        X_test = sess.run(tf.image.resize(X_test, (224, 224)))

    return X_train, y_train, X_val, y_val, X_test, y_test


if __name__ == "__main__":
    X_train, y_train, X_val, y_val, X_test, y_test = load_data()
    
    model_name = 'trainedResnet_20241016_2112'

    custom_objects = {"Adam": Adam}
    model = tf.keras.models.load_model(f"../models/{model_name}.h5", custom_objects=custom_objects, compile=False)
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Accuracy on benign test examples: {test_accuracy * 100:.2f}%")

    min_pixel_value, max_pixel_value = 0.0, 255.0
    classifier = KerasClassifier(model=model, clip_values=(min_pixel_value, max_pixel_value), use_logits=False)

    attack = FastGradientMethod(estimator=classifier, eps=0.2)

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
    model.save("../models/" + model_name + "_fgsm_robust.h5")
