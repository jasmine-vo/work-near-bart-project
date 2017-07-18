from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from model import Bart, Business, Job, connect_to_db, db
from functions import get_job_results
import datetime
from math import ceil
import os

app = Flask(__name__)

app.secret_key = "worknearbart"

app.jinja_env.undefined = StrictUndefined

gmaps = os.environ['GOOGLE_MAPS_KEY']


@app.route('/')
def index():
    """Homepage."""
    
    stations = db.session.query(Bart.station_code, Bart.name, Bart.latitude, Bart.longitude).all()

    return render_template("homepage.html",
                            stations=stations,
                            gmaps=gmaps)


@app.route('/results/<page_num>')
def display_results(page_num):
    """Displays job results."""

    stations = db.session.query(Bart.station_code, Bart.name, Bart.latitude, Bart.longitude).all()

    title = '%'.join(request.args.get('title').split())

    selected_station = request.args.get('station')

    display_per_page = int(request.args.get('display'))

    age = int(request.args.get('age'))

    current_time = datetime.datetime.utcnow()

    within_age = current_time - datetime.timedelta(days=age)

    job_results = get_job_results(selected_station, title, within_age)

    # uses current page number and display per page to slice results for pagination
    current_page_results = job_results[int(page_num) * display_per_page - display_per_page : int(page_num) * display_per_page]

    num_results = len(job_results)

    # calcuates number of page links to create
    if num_results > display_per_page:
        num_pages = int(ceil(num_results / float(display_per_page)))
    else:
        num_pages = 1

    return render_template("results.html",
                            num_pages=int(num_pages),
                            page_num=int(page_num),
                            current_page_results=current_page_results,
                            display_per_page=display_per_page,
                            title=title,
                            selected_station=selected_station,
                            age=age,
                            stations=stations,
                            gmaps=gmaps)


@app.route('/stations.json')
def get_station_info():
    """JSON information about stations"""

    stations = {
        station.station_code: {
            'stationName': station.name,
            'stationAddress': station.address,
            'stationCity': station.city,
            'stationState': station.state,
            'stationZipcode': station.zipcode,
            'stationLatitude': station.latitude,
            'stationLongitude': station.longitude,
        }
        for station in Bart.query.all()}

    return jsonify(stations) 


@app.route('/results.json')
def get_job_listings():
    """Return job results on current page in JSON format."""

    job_listings = {}

    for row in session['current_page_results']:
        job_listings[row[14]] = {
            'jobCompany': row[3],
            'jobTitle': row[2],
            'jobLatitude': row[12],
            'jobLongitude': row[13]
        }

    return jsonify(job_listings)


if __name__ == "__main__":
    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')