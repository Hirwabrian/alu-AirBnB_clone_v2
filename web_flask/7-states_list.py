#!/usr/bin/python3
""" Script that starts a Flask web application 
that displays a list of states"""

from flask import Flask, render_template
import models
from models.state import State

app = Flask(__name__)

@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays a HTML page with a list of all State objects
    in alphabetical order"""

    States = models.storage.all(State).values()
    States = sorted(States, key= lambda state: state.name)
    return render_template('7-states_list.html', States=States)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    models.storage.close()


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000)