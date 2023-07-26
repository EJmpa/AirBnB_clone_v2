#!/usr/bin/python3
"""
This module defines a Flask web application that displays states and cities.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states_list():
    """
    This function defines the route '/states'
    and displays a list of states.
    """
    states = storage.all(State)
    return render_template('9-states.html', mode='all', states=states)


@app.route('/states/<string:id>', strict_slashes=False)
def cities_by_state(id):
    """
    This function defines the route '/states/<id>'
    and displays a list of cities linked to the state with the given id.
    """
    state = storage.get(State, id)
    if state is None:
        return render_template('9-states.html', mode='none')
    return render_template('9-states.html', mode='id', states=state)


@app.teardown_appcontext
def teardown(self):
    """
    This method is called after each request and
    closes the current SQLAlchemy Session.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
