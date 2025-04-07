from flask_pymongo import PyMongo
from app import app  # Assuming your Flask app is in a file called app.py

mongo = PyMongo(app)

def init_db():
    # Insert starter data if it doesn't already exist
    if mongo.db.starter_data.count_documents({}) == 0:
        mongo.db.starter_data.insert_many([
            {"name": "Example 1", "description": "First test record"},
            {"name": "Example 2", "description": "Second test record"}
        ])
    print("Database initialized.")

if __name__ == "__main__":
    init_db()
