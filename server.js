const express = require("express");
const app = express();
const port = 3000;

// Simulated player data
const players = [
    { userId: 1, username: "PlayerOne" },
    { userId: 2, username: "PlayerTwo" },
];

// Endpoint to get player data
app.get("/api/players", (req, res) => {
    res.json(players);
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
