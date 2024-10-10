#!/usr/bin/python3
""" Starts a Flask web application to list all states and cities """
from flask import Flask, render_template
import models
from models.state import State

app = Flask(__name__)

@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """display the states and cities listed in alphabetical order"""

    States = models.storage.all(State).values()
    return render_template('8-cities_by_states.html', States=States)

@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy session """
    models.storage.close()


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000)