from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from model import Bart, Business, Job, User, Favorite, connect_to_db, db
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

    session['current_page_results'] = current_page_results
    
    num_results = len(job_results)

    # calcuates number of page links to create
    if num_results > display_per_page:
        num_pages = int(ceil(num_results / float(display_per_page)))
    else:
        num_pages = 1

    if 'user_id' in session:
        favorites = db.session.query(Favorite.job_id).filter(Favorite.user_id==session['user_id']).all()
        favorites = [fav[0] for fav in favorites]
    else:
        favorites = None

    return render_template("results.html",
                            num_pages=int(num_pages),
                            page_num=int(page_num),
                            current_page_results=current_page_results,
                            display_per_page=display_per_page,
                            title=title,
                            selected_station=selected_station,
                            age=age,
                            stations=stations,
                            gmaps=gmaps,
                            favorites=favorites)


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

    job_listings = {   
        row[12]: {
            'jobCompany': row[2],
            'jobTitle': row[1],
            'jobLatitude': row[13],
            'jobLongitude': row[14]
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

    if User.query.filter_by(email=user_email, password=user_password).first():
        user_id = User.query.filter_by(email=user_email).first().user_id
        flash('Logged in.')
        session['user_id'] = user_id

        return redirect('/')
    else:
        flash("Wrong email or password! Please register if you are a new user.")
        return redirect("/login")


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

    if User.query.filter_by(email=user_email).first() is None:
        flash('Thank you for registering! Please log-in.')

        user = User(email=user_email,
                    password=password)


        db.session.add(user)
        db.session.commit()

    else:
        flash('You already have an account.')

    return redirect('/')


@app.route('/savedjobs')
def display_saved_jobs():
    """Displays the user's saved jobs."""

    user = User.query.filter_by(user_id=session['user_id']).first()

    favorites = db.session.query(Favorite.job_id).filter(Favorite.user_id==session['user_id']).all()

    return render_template('saved_jobs.html',
                            user=user,
                            favorites=favorites)


@app.route('/processfavorite.json', methods=["POST"])
def process_favorite():
    """Add/Update favorite."""

    job_id = request.form.get("id")

    user_id = session.get("user_id")

    favorite = Favorite.query.filter_by(user_id=user_id, job_id=job_id).first()

    if favorite is not None:

        db.session.delete(favorite)

        response = { 'status': "not-saved", 'id': job_id }

    else:
        favorite = Favorite(user_id=user_id, job_id=job_id)
        db.session.add(favorite)

        response = { 'status': "saved", 'id': job_id }

    db.session.commit()

    return jsonify(response)


if __name__ == "__main__":
    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')