import os
import shutil

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket
from starlette.middleware.cors import CORSMiddleware

from core.api_core import process_and_store_image
from core.img_classifier import process_classification

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3020"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Home page successfully working"}


@app.websocket("/ws")
async def img_classification(websocket: WebSocket):
    await websocket.accept()
    i = 0
    async for predicted_category in process_classification():
        print(predicted_category, i)
        i += 1
        await websocket.send_text(predicted_category)


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):

    try:
        await process_and_store_image(file.file.read(), file.filename)
        return {"filename": file.filename, "message": "Image uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8050, reload=True)
