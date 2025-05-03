const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;

// MongoDB connection
mongoose.connect('mongodb+srv://your-mongodb-connection-string', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

const playerSchema = new mongoose.Schema({
    userId: { type: String, required: true },
    username: { type: String, required: true }
});

const Player = mongoose.model('Player', playerSchema);

app.use(bodyParser.json());

// Endpoint to add a player ID and username
app.post('/addPlayer', async (req, res) => {
    const { userId, username } = req.body;

    try {
        const newPlayer = new Player({ userId, username });
        await newPlayer.save();
        res.status(200).json({ message: 'Player added successfully' });
    } catch (error) {
        res.status(500).json({ message: 'Failed to add player', error });
    }
});

// Endpoint to get all players
app.get('/getPlayers', async (req, res) => {
    try {
        const players = await Player.find();
        res.status(200).json(players);
    } catch (error) {
        res.status(500).json({ message: 'Failed to fetch players', error });
    }
});

// Default route
app.get('/', (req, res) => {
    res.send('Roblox Tag System API');
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
