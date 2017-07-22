from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from model import Bart, Business, Job, User, Save, connect_to_db, db
from api_functions import get_job_results, get_fare
import datetime
from functions import *
from math import ceil
import os

app = Flask(__name__)

app.secret_key = "worknearbart"

app.jinja_env.undefined = StrictUndefined

gmaps = os.environ['GOOGLE_MAPS_KEY']


@app.route('/')
def index():
    """Homepage."""
    
    sf_stations = Bart.query.filter_by(station_city='San Francisco').all()

    all_stations = Bart.query.all()

    return render_template("homepage.html",
                            sf_stations=sf_stations,
                            all_stations=all_stations,
                            gmaps=gmaps)


@app.route('/results/<page_num>')
def display_results(page_num):
    """Displays job results."""

    sf_stations = Bart.query.filter_by(station_city='San Francisco').all()

    all_stations = Bart.query.all()

    title = '%'.join(request.args.get('title').split())
    selected_station = request.args.get('station')
    display_per_page = int(request.args.get('display'))
    days = int(request.args.get('days'))
    origin_station = request.args.get('origin_station')

    # Calculates the datetime by getting the current time and subtracts the
    # number of days selected by the user
    within_age = datetime.datetime.utcnow() - datetime.timedelta(days=days)

    # Gets a list of all job results returned based on the User's search criteria
    job_results = get_job_results(selected_station, title, within_age)

    # Uses current page number and display per page to slice results for pagination
    current_page_results = get_current_page_results(job_results, page_num, display_per_page)

    # Saves the current page results to session to JSONify for Google Map markers
    session['current_page_results'] = current_page_results
    
    # Calcuates number of page links to create
    num_pages = get_num_pages(len(job_results), display_per_page)

    # If origin station was entered, calculate fare amounts
    if origin_station != 'None':
        if selected_station == 'all':
            fare = {
            station.station_code: {'fare' : get_fare(origin_station,
                                                     station.station_code)
            } for station in sf_stations}

        else:
            fare = {selected_station: {'fare' : get_fare(origin_station,
                                                             selected_station)}
            }
    else:
        fare = None

    # If the user is logged in, gets a list of their saved jobs.
    if 'user_id' in session:
        saved_jobs = get_saved_from_db(session.get('user_id'))

    else:
        saved_jobs = None

    return render_template("results.html",
                            num_pages=int(num_pages),
                            page_num=int(page_num),
                            job_results=job_results,
                            current_page_results=current_page_results,
                            display_per_page=display_per_page,
                            title=title,
                            selected_station=selected_station,
                            days=days,
                            sf_stations=sf_stations,
                            gmaps=gmaps,
                            saved_jobs=saved_jobs,
                            fare=fare,
                            all_stations=all_stations)


@app.route('/stations.json')
def get_station_info():
    """Returns BART station information in JSON format."""


    stations = {
        station.station_code: {
            'stationName': station.station_name,
            'stationAddress': station.station_address,
            'stationCity': station.station_city,
            'stationState': station.station_state,
            'stationZipcode': station.station_zipcode,
            'stationLatitude': station.station_latitude,
            'stationLongitude': station.station_longitude,
        }
        for station in Bart.query.filter_by(station_city='San Francisco').all()}

    return jsonify(stations) 


@app.route('/results.json')
def get_job_listings():
    """Return job results on current page in JSON format."""

    job_listings = {   
        row[12]: {
            'jobCompany': row[2],
            'jobTitle': row[1],
            'jobLatitude': row[13],
            'jobLongitude': row[14],
            'stationName': row[5],
            'stationLatitude': row[15],
            'stationLongitude': row[16]
        }
        for row in session['current_page_results']}

    return jsonify(job_listings)


@app.route('/login')
def login_form():
    """Display login form."""

    return render_template("login_form.html")


@app.route('/login', methods=["POST"])
def login_in_process():
    """Login in process."""

    user_password = request.form.get("password")
    user_email = request.form.get("email")

    # Checks if user email entered is in database.
    user = User.query.filter(User.email == user_email).first()

    # If the user exists, checks if the password entered matches.
    if user:

        if user_password == user.password:
            user_id = user.user_id
            session['user_id'] = user_id
            flash('You are logged in as {}.'.format(user_email))

            return redirect('/')

        else:
            flash('Incorrect email or password.')

            return redirect('/login')

    else:
        flash('That email does not exist.  Please register if you are a new user.')
        
        return redirect('/login')


@app.route('/logout', methods=["POST"])
def log_out_process():
    """Log out process."""

    del session['user_id']
    flash('Logged out.')

    return redirect('/')


@app.route("/register")
def register_form():
    """Display register form."""

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Process form."""

    password = request.form.get("password")
    user_email = request.form.get("email")

    # Checks if the email already exists in the database.
    # If not, adds the user as a new user in the database.
    if User.query.filter_by(email=user_email).first() is None:
        flash('Thank you for registering! Please log-in.')

        user = User(email=user_email,
                    password=password)


        db.session.add(user)
        db.session.commit()

    else:
        flash('An account already exists with that email.')

    return redirect('/')


@app.route('/savedjobs')
def display_saved_jobs():
    """Displays the user's saved jobs."""

    user = User.query.filter_by(user_id=session.get('user_id')).first()

    saved = db.session.query(Save.job_key).filter(Save.user_id==session.get('user_id')).all()

    return render_template('saved_jobs.html',
                            user=user,
                            saved=saved)


@app.route('/processsave.json', methods=["POST"])
def process_save():
    """Add/Update saved jobs, and sends result in JSON format."""

    job_key = request.form.get("id")
    user_id = session.get("user_id")

    # Checks if the job was already favorited by the user.
    saved = Save.query.filter_by(user_id=user_id, job_key=job_key).first()

    # If the job was already favorited, deletes the saved job from the database.
    # Otherwise, adds the job to the database as a new saved job.
    if saved is not None:
        db.session.delete(saved)

        response = { 'status': "not-saved", 'id': job_key }

    else:
        saved = Save(user_id=user_id, job_key=job_key)
        db.session.add(saved)

        response = { 'status': "saved", 'id': job_key }

    db.session.commit()

    return jsonify(response)


if __name__ == "__main__":
    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')