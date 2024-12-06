import tensorflow as tf
import argparse

def load_and_show_summary(model_path):
    """
    Loads a Keras model from the specified path and displays its summary.

    Args:
        model_path (str): Path to the saved model (.h5 or SavedModel format).
    """
    try:
        # Load the model
        model = tf.keras.models.load_model(model_path)

        # Display the model's summary
        print("Model loaded successfully. Here's the summary:")
        model.summary()

    except Exception as e:
        print(f"Error loading model: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load a Keras model and display its summary.")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the saved Keras model (.h5 or SavedModel).")
    args = parser.parse_args()

    load_and_show_summary(args.model_path)
