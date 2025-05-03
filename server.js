const express = require("express");
const app = express();
const port = process.env.PORT || 3000;

// Initialize an empty array to store players' data
let players = [];

// Middleware to parse JSON bodies
app.use(express.json());

// Endpoint to receive player data and add it to the list
app.post("/", (req, res) => {
    const { userId, username } = req.body;
    
    // Check if the player already exists, if not, add them
    const existingPlayer = players.find(player => player.userId === userId);
    if (!existingPlayer) {
        players.push({ userId, username });
        console.log(`Player added: ${username}`);
    }

    res.status(200).send("Player data received");
});

// Endpoint to show all player data (this will be at the root of the website)
app.get("/", (req, res) => {
    res.json(players); // Return the list of players
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
