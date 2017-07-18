from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from model import Bart, Business, Job, connect_to_db, db


app = Flask(__name__)

app.secret_key = "worknearbart"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    stations = db.session.query(Bart.station_code, Bart.name, Bart.latitude, Bart.longitude).all()

    return render_template("homepage.html",
                            stations=stations)


if __name__ == "__main__":
    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')