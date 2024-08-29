import os
from pathlib import Path

from config import load_config

global_config = load_config()


async def process_and_store_image(file_data: bytes, filename: str) -> str:

    data_input_dir = global_config["data"]["input"]

    os.makedirs(data_input_dir, exist_ok=True)
    for existing_file in Path(data_input_dir).glob("*"):
        if existing_file.name != ".gitkeep":
            existing_file.unlink()

    file_path = os.path.join(data_input_dir, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file_data)

    return file_path
