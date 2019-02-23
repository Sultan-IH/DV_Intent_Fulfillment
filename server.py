from flask import Flask

app = Flask(__name__)


@app.before_request
def logger():
    print("here is the request: ", request)
