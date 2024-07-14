import asyncio
import json
import logging
import os
from typing import List, Optional

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from config import load_config
from messaging import get_rabbitmq_connection, publish_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    all_files = [f for f in os.listdir("data_input") if f.endswith((".jpg", ".jpeg"))]
    filepath = all_files[0] if all_files else None
    return filepath


async def process_classification():
    previous_filepath = _get_filepath()
    current_filepath = None
    task = None
    while True:
        if not current_filepath or (current_filepath != previous_filepath):
            if current_filepath is not None:
                previous_filepath = current_filepath
            if task is not None and not task.done():
                task.cancel()  # Cancel previous task if it's still running
            final_filepath = os.path.join(global_config["data"]["input"], previous_filepath)
            task = asyncio.create_task(classifier(final_filepath))
        yield in_mem_db.get("predicted_category", "")
        current_filepath = _get_filepath()
        await asyncio.sleep(4)


async def classifier(img_filepath):

    model = load_model(global_config["models"]["paths"]["model"], compile=False)
    img = preprocess_image(img_filepath)

    prediction = model.predict(img)
    predicted_index = prediction.argmax()

    labels_dir = label_names(global_config["models"]["paths"]["indices"])

    hero_labels = sorted(labels_dir)
    predicted_category = hero_labels[predicted_index]

    in_mem_db["predicted_category"] = predicted_category

    # Create tasks for publishing messages without awaiting them
    asyncio.create_task(
        publish_message(event={"message": "New hero detected", "hero": predicted_category}, routing_key="events")
    )
    asyncio.create_task(
        publish_message(
            event={"message": "Hero smashing", "hero": predicted_category}, routing_key=f"hero.{predicted_category}"
        )
    )
