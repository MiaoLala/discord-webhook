from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Discord Flask Web Server Running!"

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))