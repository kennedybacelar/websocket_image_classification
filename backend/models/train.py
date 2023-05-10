import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from models.model import build_model
from config import load_config

global_config = load_config()


def train():
    os.environ[  # Set TensorFlow logging level to suppress warnings
        "TF_CPP_MIN_LOG_LEVEL"
    ] = "3"

    data_directory = (
        global_config.get("train", {})
        .get("resources", {})
        .get("train_dataset", "train_dataset")
    )

    # Set the parameters for data preprocessing and augmentation
    image_size = (224, 224)
    batch_size = global_config.get("train", {}).get("params", {}).get("batch_size", 32)
    epochs = global_config.get("train", {}).get("params", {}).get("epochs", 10)

    validation_split = (
        global_config.get("train", {}).get("params", {}).get("validation_split", 0.4)
    )

    # Create an ImageDataGenerator for data preprocessing and augmentation
    datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=validation_split,
    )

    # Load the training dataset
    train_dataset = datagen.flow_from_directory(
        data_directory,
        target_size=image_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="training",
    )

    # Load the validation dataset
    validation_dataset = datagen.flow_from_directory(
        data_directory,
        target_size=image_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="validation",
    )

    # Input shape of the model: (height=224, width=224, color_channels=3)
    # The third dimension of the input shape (i.e., 3) corresponds to the 3 color channels (Red, Green, Blue) of the RGB color space.
    model = build_model(
        input_shape=(224, 224, 3), num_classes=train_dataset.num_classes
    )

    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    model.fit(train_dataset, validation_data=validation_dataset, epochs=epochs)

    save_model(model)
    save_class_indices_as_json(train_dataset.class_indices)


def save_model(model):
    filename = (
        global_config.get("models", {})
        .get("paths", {})
        .get("model", "models/heroes.h5")
    )
    model.save(filename)


def save_class_indices_as_json(class_indexes: dict):
    # Save the class indices mapping as a JSON file
    filename = (
        global_config.get("models", {})
        .get("paths", {})
        .get("indices", "models/heroes_class_indices.json")
    )

    with open(filename, "w") as file:
        json.dump(class_indexes, file)


if __name__ == "__main__":
    train()
