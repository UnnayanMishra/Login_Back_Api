const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());

// MySQL connection
const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  port: 3306
});

db.connect((err) => {
  if (err) {
    console.error('Database connection error:', err.message);
  } else {
    console.log('Connected to MySQL database');
  }
});

// API route
app.post('/verify-user', (req, res) => {
  const { username } = req.body;
  const query = 'SELECT link FROM user_credentials WHERE user_name = ?';

  db.query(query, [username], (err, results) => {
    if (err) {
      console.error('Query error:', err.message);
      return res.status(500).json({ error: 'Database error' });
    }

    if (results.length > 0) {
      res.json({ exists: true, link: results[0].link });
    } else {
      res.json({ exists: false });
    }
  });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
