const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

let players = {};

app.post("/add", (req, res) => {
  const { userId, username } = req.body;
  if (userId && username) {
    players[userId] = { username };
    res.status(200).send({ message: "Player added!" });
  } else {
    res.status(400).send({ message: "Invalid data!" });
  }
});

app.get("/players", (req, res) => {
  res.status(200).json(players);
});

app.get("/", (req, res) => {
  res.send("✅ Server is running!");
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
