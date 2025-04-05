const { MongoClient } = require('mongodb');

const uri = "mongodb://localhost:27017";
const client = new MongoClient(uri);

async function run() {
  try {
    await client.connect();
    const database = client.db('securedb');
    const messages = database.collection('messages');
    await messages.insertMany([
      { text: "Hello from MongoDB!" },
      { text: "This app uses HTTPS via Let's Encrypt" },
      { text: "Deployed securely with Ansible and Jenkins" }
    ]);
    console.log("Data inserted successfully");
  } finally {
    await client.close();
  }
}

run().catch(console.dir);
