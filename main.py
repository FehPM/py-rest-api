from flask import Flask
app = Flask(__name__)

app.config["DEBUG"] = True
@app.route("/", methods=["GET"])
def index():
    return "<h1>GUD</h1>"


if __name__ == "__main__":
    app.run()
