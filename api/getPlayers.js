// api/getPlayers.js

import { MongoClient } from 'mongodb';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    // Connect to MongoDB (replace with your MongoDB URI)
    const client = await MongoClient.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    const db = client.db();
    const playersCollection = db.collection('players');

    // Retrieve all players from the database
    const players = await playersCollection.find().toArray();

    client.close();

    res.status(200).json(players); // Return the players as JSON
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}
