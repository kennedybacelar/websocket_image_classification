from fastapi import FastAPI, WebSocket
import uvicorn
from core.img_classifier import process_classification

app = FastAPI()


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


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8050, reload=True)
