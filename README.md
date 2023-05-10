# Project Name

## Description

This project consists of a backend and a frontend. The backend is built with FastAPI, which provides a home page, and a WebSocket endpoint to communicate with the frontend. The endpoint "/ws" receives an image classification result and sends it to the frontend in real-time using WebSocket.

The backend uses TensorFlow and Keras libraries to perform image classification. It has a file called "img_classifier.py" which contains functions to preprocess images, load a trained model, and predict the category of an image.

The backend has an asynchronous generator function called "process_classification", which reads a directory to check for new image files, and when it finds one, processes the image with the "classifier" function. The "classifier" function loads the model and predicts the category of the image. Finally, the "process_classification" function yields the predicted category to the WebSocket endpoint, which sends it to the frontend.

The frontend is built with Express.js and consists of an HTML file that displays a default image and a quote. It has three endpoints: "/", "/get-random-filepath/:folderName", and "/get-random-quote/:folderName".

The "/" endpoint sends the HTML file to the client, while the "/get-random-filepath/:folderName" and "/get-random-quote/:folderName" endpoints receive a folder name and return a randomly selected image file path and quote, respectively.

The backend runs on port 8050 and the frontend runs on port 3020. The frontend uses WebSocket to communicate with the backend and display the predicted image category in real-time.

## Prerequisites

List of prerequisites required to run the project.

## Installation

If you run it on docker no manual installation is required. Just enter the docker-compose command in the following section.

If you run as independent servers:

At the backend folder run:
```bash
pip install -r requirements.txt
```
At the frontend folder run:
```bash
npm install
```

## Usage

Instructions on how to use the project.

The project can be run as a whole piece through docker by entering the command:

```bash
docker-compose up --build
```

Or it can be started as a backend and frontend separated through the commands below:


To spin off the server, navigate to the backend folder and run:

```bash
python -m api.main
```

To start the frontend, navigate to the root folder and run:

```bash
npm start
```

If you want to train the models, run the following command in the backend folder:

```bash
python -m models.train
```

## Contributing

Guidelines for contributing to the project.

## License

Information about the project's license.