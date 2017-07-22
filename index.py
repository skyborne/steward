from flask import Flask
from flask import request

from server import (
    generate_key,
)


app = Flask(__name__)

@app.route("/key/")
def key():
    return "{}".format(generate_key())
