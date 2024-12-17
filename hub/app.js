const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const app = express();
const PORT = 3000;

app.use(bodyParser.json());

// In-memory database (text file)
const dbFilePath = 'users.txt';

// Helper functions for reading/writing users
const readUsersFromFile = () => {
    if (!fs.existsSync(dbFilePath)) {
        return [];
    }
    const data = fs.readFileSync(dbFilePath, 'utf-8');
    return data.split('\n').filter(Boolean).map(line => JSON.parse(line));
};

const writeUsersToFile = (users) => {
    fs.writeFileSync(dbFilePath, users.map(user => JSON.stringify(user)).join('\n'));
};

// User Registration
app.post('/add_user', (req, res) => {
    const { email, age } = req.body;
    if (!email || !age) {
        return res.status(400).send('Email and age are required.');
    }
    const users = readUsersFromFile();
    users.push({ email, age });
    writeUsersToFile(users);
    res.status(201).send('User registered successfully.');
});

// Retrieve User Information
app.get('/user/:email', (req, res) => {
    const users = readUsersFromFile();
    const user = users.find(u => u.email === req.params.email);
    if (!user) {
        return res.status(404).send('User not found.');
    }
    res.json(user);
});

// Update User Information
app.put('/user/:email', (req, res) => {
    const { email } = req.params;
    const { age } = req.body;
    const users = readUsersFromFile();
    const userIndex = users.findIndex(u => u.email === email);
    if (userIndex === -1) {
        return res.status(404).send('User not found.');
    }
    if (age) {
        users[userIndex].age = age;
        writeUsersToFile(users);
        return res.send('User updated successfully.');
    }
    res.status(400).send('Age is required for update.');
});

// Delete User Information
app.delete('/user/:email', (req, res) => {
    const users = readUsersFromFile();
    const updatedUsers = users.filter(u => u.email !== req.params.email);
    if (users.length === updatedUsers.length) {
        return res.status(404).send('User not found.');
    }
    writeUsersToFile(updatedUsers);
    res.send('User deleted successfully.');
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});