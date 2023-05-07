import os
import asyncio
import json
from typing import Optional, List
from config import load_config
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

global_config = load_config()
in_mem_db = {}


def label_names(file_name):
    with open(file_name, "r") as file:
        data = json.load(file)
    return list(data.keys())


def preprocess_image(img_filepath):
    img = image.load_img(img_filepath, target_size=(224, 224))
    img = image.img_to_array(img)
    img = img / 255.0  # Normalize pixel values between 0 and 1
    img = img.reshape((1,) + img.shape)
    return img


def get_data_input_filepath() -> Optional[str]:
    return os.listdir()[0] if os.listdir() else None


def _get_filepath():
    return os.listdir("data_input")[0] if os.listdir("data_input") else None


async def process_classification():
    previous_filepath = _get_filepath()
    current_filepath = None
    task = None
    while True:
        if not current_filepath or (current_filepath != previous_filepath):
            if task is not None and not task.done():
                task.cancel()  # Cancel previous task if it's still running
            final_filepath = os.path.join(
                global_config["data"]["input"], previous_filepath
            )
            task = asyncio.create_task(classifier(final_filepath))
        yield in_mem_db.get("predicted_category")
        current_filepath = _get_filepath()
        await asyncio.sleep(1)


async def classifier(img_filepath):

    model = load_model(global_config["models"]["paths"]["model"])
    img = preprocess_image(img_filepath)

    prediction = model.predict(img)
    predicted_index = prediction.argmax()

    labels_dir = label_names(global_config["models"]["paths"]["indices"])

    hero_labels = sorted(labels_dir)
    predicted_category = hero_labels[predicted_index]

    in_mem_db["predicted_category"] = predicted_category
    # return predicted_category


async def testando():
    i = 0
    while True:
        yield f"Testando {i}"
        await asyncio.sleep(1)
        i += 1
