from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId  # This is for handling ObjectId in MongoDB

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.devdb  
collection = db.starter_data  

# Function to convert ObjectId to string
def bson_to_dict(bson_obj):
    # This function helps to convert ObjectId into string for JSON serialization
    bson_obj['_id'] = str(bson_obj['_id'])
    return bson_obj

@app.route('/')
def home():
    # Get all records from MongoDB and convert to list
    data = list(collection.find())
    # Convert ObjectId to string for JSON serialization
    data = [bson_to_dict(item) for item in data]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
