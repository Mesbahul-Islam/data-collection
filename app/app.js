const express = require('express');
const mysql = require('mysql2');
const dotenv = require('dotenv');

dotenv.config({ path: './api_handling/.env' });

const app = express();
const port = 3000;

// Serve static files from the 'public' directory
app.use(express.static('public'));

const connection = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT
});

connection.connect((err) => {
    if (err) {
        console.log(err);
    } else {
        console.log('Connected to the database');
    }
});

app.get('/champion-stats', (req, res) => {
    const { champion } = req.query;
    let query = 'SELECT championName, winPercent, totalGames FROM win_percent_by_champion';
    const queryParams = [];

    if (champion) {
        query += ' WHERE championName = ?';
        queryParams.push(champion);
    }

    connection.query(query, queryParams, (err, results) => {
        if (err) {
            console.error('Error fetching data', err);
            res.status(500).send('Error fetching data');
            return;
        }
        const data = results[0]; // Get the first result
        console.log(data); // Log the value of data
        res.json({ data }); // Return only the first result
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});