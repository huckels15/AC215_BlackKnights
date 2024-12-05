import tensorflow as tf
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent as PGD, DeepFool, SquareAttack as Square
from art.estimators.classification import KerasClassifier
from tensorflow.keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import cv2
import json

tf.compat.v1.disable_eager_execution()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def preprocess_data(data_path, batch_size, img_height, img_width, channels):
    data = []
    class_mapping = {}
    class_index = 0

    for class_name in os.listdir(data_path):
        class_path = os.path.join(data_path, class_name)
        if os.path.isdir(class_path):
            if class_name not in class_mapping:
                class_mapping[class_name] = class_index
                class_index += 1
            
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                data.append((img_path, class_mapping[class_name]))

    np.random.shuffle(data)

    images, labels = [], []
    for img_path, class_id in data:
        if channels == 1:
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Grayscale
        elif channels == 3:
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)  # RGB

        img = cv2.resize(img, (img_height, img_width))
        if channels == 1:
            img = img[..., np.newaxis]
        images.append(img / 255.0)
        labels.append(class_id)

        if len(images) == batch_size:
            yield np.array(images), to_categorical(labels, num_classes=len(class_mapping))
            images, labels = [], []

    if images:
        yield np.array(images), to_categorical(labels, num_classes=len(class_mapping))



def plot_samples(num_samples, x_test, x_test_adv, y_test, predictions_adv):
    """
    Function to plot a sample before and after adversarial perturbations.
    """
    os.makedirs("figures", exist_ok=True)

    for i in range(num_samples):
        true_label = np.argmax(y_test[i])
        adv_pred_label = np.argmax(predictions_adv[i])

        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].imshow((x_test[i] * 255).astype(np.uint8))
        ax[0].set_title(f"Original\nTrue: {true_label}", fontsize=12, color="green")
        ax[0].axis('off')

        ax[1].imshow((x_test_adv[i] * 255).astype(np.uint8))
        ax[1].set_title(f"Adversarial\nTrue: {true_label}\nPred: {adv_pred_label}", fontsize=12, color="red")
        ax[1].axis('off')

        fig.suptitle(f"Example {i + 1}", fontsize=14, fontweight="bold")
        plt.savefig(f"figures/example_{i + 1}_original_vs_adversarial.png")
        plt.close(fig)

    return "figures/example_1_original_vs_adversarial.png"



def parse_args():
    """
    Parse command line arguments.
    """
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
    parser.add_argument(
        "--eps",
        type=float, 
        default=0.2, 
        help="Perturbation magnitude for FGSM/PGD"
    )
    parser.add_argument(
        "--eps_step", 
        type=float, 
        default=0.01, 
        help="Step size for PGD"
    )
    parser.add_argument(
        "--max_iter", 
        type=int, 
        default=50, 
        help="Maximum iterations for attacks"
    )
    parser.add_argument(
        "--model_path",
        type=str
    )
    parser.add_argument(
        "--data_path",
        type=str
    )
    parser.add_argument(
        "--height",
        type=int
    )
    parser.add_argument(
        "--width",
        type=int
    )
    parser.add_argument(
        "--channels",
        type=int
    )
    args = parser.parse_args()
    return vars(args)


def run(uploaded_model_path, uploaded_data_path, attack_params, img_height, img_width, channels):
    """
    Run adversarial attacks on the uploaded model and data.
    """
    model = tf.keras.models.load_model(uploaded_model_path, compile=False)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    batch_size = 64
    data_generator = preprocess_data(uploaded_data_path, batch_size, img_height, img_width, channels)
    x_test, y_test = next(data_generator)

    classifier = KerasClassifier(model=model, clip_values=(0.0, 1.0), use_logits=False)

    predictions = classifier.predict(x_test)
    clean_accuracy = np.mean(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1))

    if attack_params["fgsm"]:
        attack = FastGradientMethod(estimator=classifier, eps=attack_params["eps"])
    elif attack_params["pgd"]:
        attack = PGD(estimator=classifier, eps=attack_params["eps"], eps_step=attack_params["eps_step"], max_iter=attack_params["max_iter"])
    elif attack_params["deepfool"]:
        attack = DeepFool(classifier=classifier, max_iter=attack_params["max_iter"])
    elif attack_params["square"]:
        attack = Square(estimator=classifier, eps=attack_params["eps"], max_iter=attack_params["max_iter"])
    else:
        raise ValueError("No valid attack specified.")

    x_test_adv = attack.generate(x=x_test)
    adv_predictions = classifier.predict(x_test_adv)
    adv_accuracy = np.mean(np.argmax(adv_predictions, axis=1) == np.argmax(y_test, axis=1))

    path = plot_samples(1, x_test, x_test_adv, y_test, adv_predictions)

    results = {
        "reg_acc": clean_accuracy * 100,
        "adv_acc": adv_accuracy * 100,
        "figure": path
    }
    print(json.dumps(results))
    return results


if __name__ == "__main__":
    args = parse_args()
    
    uploaded_model_path = args['model_path']
    uploaded_data_path = args['data_path']
    img_height = args['width']
    img_width = args['height']
    channels = args['channels']

    run(uploaded_model_path, uploaded_data_path, args, img_height, img_width,channels)