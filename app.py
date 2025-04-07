from flask import Flask, jsonify

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    # Return the simple message as plain text for now
    return "Secure DevOps app deployed with verified artifact! This application was built by Collins Ifeoma Collins"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

