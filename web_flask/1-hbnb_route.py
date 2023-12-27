#!/usr/bin/python3
""" Start a Flask web application """
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Return Hello HBNB! from 0.0.0.0:5000 """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnh():
    """ Returns HBNH from 0.0.0.0:5000/hbnb """
    return "HBNB"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
