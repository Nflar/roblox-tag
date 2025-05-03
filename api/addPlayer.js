// api/addPlayer.js

import { MongoClient } from 'mongodb';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    // Connect to MongoDB (replace with your MongoDB URI)
    const client = await MongoClient.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    const db = client.db();
    const playersCollection = db.collection('players');
    
    // Parse the incoming request body
    const { userId, username } = req.body;

    // Save the player data to the database
    await playersCollection.insertOne({ userId, username });

    client.close();

    res.status(200).json({ message: 'Player added successfully' });
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}
