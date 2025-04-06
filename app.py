from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return (
        "Secure DevOps app deployed with verified artifact!<br><br>"
        "This application was built by Collins Ifeoma Lilicent<br>"
        "Accessible via HTTPS port 443"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
