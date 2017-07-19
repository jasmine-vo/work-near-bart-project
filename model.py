from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bart(db.Model):
    """Bart stations."""

    __tablename__ = "stations"

    station_code = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    latitude = db.Column(db.String(15), nullable=False)
    longitude = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Bart station_code=%s name=%s>" % (self.station_code, self.name)


class Business(db.Model):
    """Business locations."""

    __tablename__ = "businesses"

    business_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.String(15), nullable=False)
    longitude = db.Column(db.String(15), nullable=False)
    distance = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    logo_url = db.Column(db.String(200), nullable=True)
    rating = db.Column(db.String(20), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    glassdoor_url = db.Column(db.String(200), nullable=True)
    station_code = db.Column(db.String(4),
                             db.ForeignKey('stations.station_code'),
                             nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Business business_id=%s name=%s station_code=%s>"
        return s % (self.business_id,
                    self.name,
                    self.station_code)


class Job(db.Model):
    """Job details."""

    __tablename__ = "jobs"

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    duration_posted = db.Column(db.String(15), nullable=False)
    business_id = db.Column(db.Integer,
                            db.ForeignKey("businesses.business_id"),
                            nullable=False)
    business = db.relationship("Business",
                            backref=db.backref("jobs"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Job job_id=%s title=%s business_id=%s>"
        return s % (self.job_id, self.title, self.business_id)


class User(db.Model):
    """Users."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Favorite(db.Model):
    """Job listings user favorited."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    job_id = db.Column(db.Integer,
                         db.ForeignKey('jobs.job_id'))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User",
                            backref=db.backref("favorites"))

    job = db.relationship("Job",
                            backref=db.backref("favorites"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Favorite favorite_id=%s job_id=%s user_id=%s>"
        return s % (self.favorite_id, self.job_id, self.user_id)


# def example_data():
#     """Create sample data"""

#     Bart.query.delete()
#     Business.query.delete()
#     Job.query.delete()
#     User.query.delete()
#     Favorite.query.delete()

#     emb = Bart(station_code="EMBR",
#                        name="Embarcadero",
#                        address="",
#                        city="San Francisco",
#                        state="CA",
#                        zipcode="",
#                        latitude="",
#                        longitude="")

#     mon = Bart(station_code="MONT",
#                        name="Montgomery",
#                        address="",
#                        city="San Francisco",
#                        state="CA",
#                        zipcode="",
#                        latitude="",
#                        longitude="")

#     google = Business(business_id=1,
#                       name="Google",
#                       address="345 Spear St",
#                       latitude="37.790052",
#                       longitude="-122.390184",
#                       distance="0.5 mi",
#                       duration="11 mins",
#                       logo_url="https://media.glassdoor.com/sqll/9079/google-squarelogo-1441130773284.png",
#                       rating="4.4",
#                       industry="Information Technology",
#                       glassdoor_url="http://www.glassdoor.com/Reviews/Employee-Review-Google-RVW15868147.htm",
#                       station_code="EMBR")

#     udacity = Business(business_id=2,
#                       name="Udacity",
#                       address="653 Harrison St",
#                       latitude="37.783158",
#                       longitude="-122.396115",
#                       distance="0.6 mi",
#                       duration="13 mins",
#                       logo_url="https://media.glassdoor.com/sqll/659776/udacity-squarelogo-1458083545831.png",
#                       rating="4.5",
#                       industry="Education",
#                       glassdoor_url="https://www.glassdoor.com/Reviews/san-francisco-udacity-reviews-SRCH_IL.0,13_IM759_KE14,21.htm",
#                       station_code="MONT")

#     se = Job(job_id=1,
#             title="Software Engineer",
#             url="http://www.indeed.com/rc/clk?jk=ac95291e795c6aab",
#             date_posted=,
#             duration_posted=
#             business_id=1)

#     se2 = Job(job_id=2,
#             title="Software Engineer, Growth",
#             url="http://www.indeed.com/rc/clk?jk=d3850706e430f9f5",
#             date_posted=,
#             duration_posted=
#             business_id=2)

#     test_user = User(user_id=1,
#                      email="test@test.com",
#                      password="test")

#     favorite = Favorite(favorite_id=1,
#                         job_id=1,
#                         user_id=1)

#     db.session.add_all([emb, mon, google, udacity, se, se2, test_user, favorite])
#     db.session.commit()


##############################################################################


def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///hbproject'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
