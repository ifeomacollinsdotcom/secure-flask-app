from flask import Flask, render_template
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGODB_URI", "mongodb://username:password@localhost:172.31.44.87/securedb")

# Initialize MongoDB with TLS (for production)
client = MongoClient(
    app.config["MONGO_URI"],
    tls=True,
    tlsAllowInvalidCertificates=False  # Disable in production for valid certs
)
db = client.securedb
collection = db.messages

# Rate limiting
limiter = Limiter(app, key_func=get_remote_address)

@app.route("/")
@limiter.limit("10 per minute")  # Optional: Adjust limits as needed
def index():
    try:
        messages = list(collection.find({}))
        return render_template("index.html", messages=messages)
    except PyMongoError as e:
        return render_template("error.html", error="Database error"), 500
    except Exception as e:
        return render_template("error.html", error="Server error"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG", "False") == "True")

