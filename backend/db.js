const { MongoClient } = require("mongodb");

const uri = "";
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

let collection;

const connectToDatabase = async () => {
  try {
    await client.connect();
    console.log("Connected to MongoDB Atlas");
    collection = client.db("PROJECT").collection("Recieved_data");
  } catch (error) {
    console.error("Failed to connect to MongoDB Atlas", error);
    throw error;
  }
};

const getCollection = () => {
  if (!collection) {
    throw new Error("Database not initialized");
  }
  return collection;
};

module.exports = { connectToDatabase, getCollection };
