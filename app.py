from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # The expected message to display
    message = '''
    <html>
        <body>
            <h1>Secure DevOps app deployed with verified artifact!</h1>
            <p>This application was built by Collins Ifeoma Collins</p>
        </body>
    </html>
    '''
    return message  # Return the HTML message as a response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
