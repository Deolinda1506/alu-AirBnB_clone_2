#!/usr/bin/python3
"""
Starts a Flask application to display states and cities.

Routes:
    /states: Displays a list of all states with their IDs.
    /states/<state_id>: Displays cities for a specific state based on state_id.

Functions:
    states(state_id=None):
        Retrieves states and optionally cities based on state_id.
        Renders data using the 9-states.html template.

    teardown_db(exception):
        Closes the storage session after each request.

Usage:
    Start the application using 'python3 -m web_flask.9-states'.
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)

@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """
    Route to display states and cities.

    Args:
        state_id (str): Optional state ID to filter cities by.

    Returns:
        str: Rendered HTML template (9-states.html) with states and cities data.
    """
    states = storage.all("State")
    if state_id is not None:
        state_id = 'State.' + state_id
    return render_template('9-states.html', states=states, state_id=state_id)

@app.teardown_appcontext
def teardown_db(exception):
    """
    Teardown function to close the storage session.

    Args:
        exception: Exception object raised during request handling.
    """
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
