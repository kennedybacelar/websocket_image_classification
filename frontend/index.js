const path = require('path');
const express = require('express')
const fs = require('fs');
const app = express()
const port = 3020

const isDocker = process.env.IS_DOCKER === 'true'


app.use(express.static('public'));
app.use('/css', express.static(path.join(__dirname, 'css')));

const getRandFilePath = (folderName) => {
    const folderPath = path.join(__dirname, 'public', 'images_ext_storage_mock', folderName);
    const files = fs.readdirSync(folderPath);
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif']; // List of image file extensions
    const imageFiles = files.filter(file => imageExtensions.includes(path.extname(file)));
    const randomImageFile = imageFiles[Math.floor(Math.random() * imageFiles.length)];
    return path.join('/', 'images_ext_storage_mock', folderName, randomImageFile);
};

const getRandomQuote = (folderName) => {
    const quotesFilePath = path.join(__dirname, 'public', 'images_ext_storage_mock', '_quotes', folderName + '.txt');
    const quotes = fs.readFileSync(quotesFilePath, { encoding: 'utf8' }).split('\n');
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    return randomQuote.trim();
};


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
})

app.get('/get-random-filepath/:folderName', (req, res) => {
    const folderName = req.params.folderName;
    const filePath = getRandFilePath(folderName);
    res.send(filePath);
});

app.get('/get-random-quote/:folderName', (req, res) => {
    const folderName = req.params.folderName;
    const randomQuote = getRandomQuote(folderName);
    res.send(randomQuote);
})

app.get('/backend-prefix', (req, res) => {
    const hostname = isDocker ? 'backend' : 'localhost'
    res.send(hostname)
})

app.listen(port, '0.0.0.0', () => {
    console.log(`Server listening on port ${port}`)
})