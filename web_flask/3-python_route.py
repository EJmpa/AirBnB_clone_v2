#!/usr/bin/python3
"""
This module defines a Flask web application.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    This function defines the route '/' and displays "Hello HBNB!".
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    This function defines the route '/hbnb' and displays "HBNB".
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_with_text(text):
    """
    This function defines the route '/c/<text>' and displays "C "
    followed by the value of the text variable
    (replace underscore _ symbols with a space).
    """
    return "C {}".format(text.replace("_", " "))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_with_text(text="is cool"):
    """
    This function defines the route '/python/<text>' and displays "Python "
    followed by the value of the text variable
    (replace underscore _ symbols with a space). If no text is provided,
    it defaults to "is cool".
    """
    return "Python {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
