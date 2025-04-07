from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.devdb  
collection = db.starter_data  

@app.route('/')
def home():
    # Get all records from MongoDB
    data = list(collection.find())
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
