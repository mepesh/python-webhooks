from flask import Flask

# Initialize application
app = Flask(__name__)


@app.route("/")
def hello():
    return "Flask setup"

if __name__ == '__main__':
    app.run()
