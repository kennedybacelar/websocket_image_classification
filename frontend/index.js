const path = require('path');
const express = require('express')
const fs = require('fs');
const app = express()
const port = 3020

app.use(express.static('public'));

const getRandFilePath = (folderName) => {
    const folderPath = path.join(__dirname, 'public', 'images_ext_storage_mock', folderName);
    const files = fs.readdirSync(folderPath);
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif']; // List of image file extensions
    const imageFiles = files.filter(file => imageExtensions.includes(path.extname(file)));
    const randomImageFile = imageFiles[Math.floor(Math.random() * imageFiles.length)];
    return path.join('/', 'images_ext_storage_mock', folderName, randomImageFile);
};


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
})

app.get('/get-random-filepath/:folderName', (req, res) => {
    const folderName = req.params.folderName;
    const filePath = getRandFilePath(folderName);
    res.send(filePath);
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`)
})