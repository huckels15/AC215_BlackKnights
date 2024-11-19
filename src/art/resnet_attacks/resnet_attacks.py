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

def load_data():
    data = pd.read_csv("../data/dvc_store_csvs_hmnist_28_28_RGB.csv")
    y = data['label']
    X = data.drop(columns= ['label'])

    X = X.values.reshape(-1, 28, 28, 3)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.1)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2)

    y_train = to_categorical(y_train, num_classes=7)
    y_val = to_categorical(y_val, num_classes=7)
    y_test = to_categorical(y_test, num_classes=7)

    with tf.compat.v1.Session() as sess:
        X_train_resize = sess.run(tf.image.resize(X_train, (224, 224)))
        X_val_resize = sess.run(tf.image.resize(X_val, (224, 224)))
        X_test_resize = sess.run(tf.image.resize(X_test, (224, 224)))
    
    train_gen = train_datagen.flow(X_train_resize, y_train, batch_size=64)
    val_gen = test_datagen.flow(X_val_resize, y_val, batch_size=64)
    test_gen = test_datagen.flow(X_test_resize, y_test, batch_size=64)
    return train_gen, val_gen, test_gen


def plot_samples(num_samples, x_test, x_test_adv, y_test, predictions_adv):
    class_map = {
        0: 'Melanocytic nevi',
        1: 'Melanoma',
        2: 'Benign keratosis',
        3: 'Basal cell carcinoma',
        4: 'Actinic keratoses',
        5: 'Vascular lesions',
        6: 'Dermatofibroma'
    }
    
    for i in range(num_samples):
        true_label = class_map[np.argmax(y_test[i])]
        adv_pred_label = class_map[np.argmax(predictions_adv[i])]
        
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        
        ax[0].imshow(x_test[i].astype(np.uint8))
        ax[0].set_title(f"Original\nTrue: {true_label}", fontsize=12, color="green")
        ax[0].axis('off')
        
        ax[1].imshow(x_test_adv[i].astype(np.uint8))
        ax[1].set_title(f"Adversarial\nTrue: {true_label}\nPred: {adv_pred_label}", fontsize=12, color="red")
        ax[1].axis('off')
        
        fig.suptitle(f"Example {i + 1}", fontsize=14, fontweight="bold")
        plt.savefig(f"figures/example_{i+1}_original_vs_adversarial.png")
        plt.show()

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

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator()
_, _, test_gen = load_data()
custom_objects = {"Adam": Adam}

model = tf.keras.models.load_model("../models/trainedResnet_20241016_2143.h5", custom_objects=custom_objects, compile=False)
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

min_pixel_value, max_pixel_value = 0.0, 255.0
classifier = KerasClassifier(model=model, clip_values=(min_pixel_value, max_pixel_value), use_logits=False)

x_test, y_test = next(test_gen) 
predictions = classifier.predict(x_test)
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

x_test_adv = attack.generate(x=x_test)

predictions_adv = classifier.predict(x_test_adv)
accuracy_adv = np.sum(np.argmax(predictions_adv, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print("Accuracy on adversarial test examples: {:.2f}%".format(accuracy_adv * 100))

plot_samples(1, x_test, x_test_adv, y_test, predictions_adv)