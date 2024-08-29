import os

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Set TensorFlow logging level to suppress warnings


def build_model(input_shape, num_classes):
    base_model = MobileNetV2(input_shape=input_shape, include_top=False)
    x = GlobalAveragePooling2D()(base_model.output)
    output = Dense(num_classes, activation="softmax")(x)
    model = tf.keras.models.Model(inputs=base_model.input, outputs=output)
    return model
