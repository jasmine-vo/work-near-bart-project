from flask_sqlalchemy import SQLAlchemy
import datetime

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

    job_key = db.Column(db.String(20), primary_key=True)
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

        s = "<Job job_key=%s title=%s business_id=%s>"
        return s % (self.job_key, self.title, self.business_id)


class User(db.Model):
    """Users."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Save(db.Model):
    """Job listings user saved."""

    __tablename__ = "saved"

    save_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    job_key = db.Column(db.String(20),
                         db.ForeignKey('jobs.job_key'))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User",
                            backref=db.backref("saved"))

    job = db.relationship("Job",
                            backref=db.backref("saved"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Save saved_id=%s job_key=%s user_id=%s>"
        return s % (self.saved_id, self.job_key, self.user_id)


def example_data():
    """Create sample data"""

    Save.query.delete()
    User.query.delete()
    Job.query.delete()
    Business.query.delete()
    Bart.query.delete()

    emb = Bart(station_code="EMBR",
               name="Embarcadero",
               address="298 Market Street",
               city="San Francisco",
               state="CA",
               zipcode="94111",
               latitude="37.792874",
               longitude="-122.397020")

    db.session.add(emb)

    mon = Bart(station_code="MONT",
               name="Montgomery",
               address="598 Market Street",
               city="San Francisco",
               state="CA",
               zipcode="94104",
               latitude="37.789405",
               longitude="-122.401066")

    db.session.add(mon)

    db.session.commit()

    abc = Business(business_id=1,
                    name="ABC, Inc.",
                    address="345 Spear St",
                    latitude="37.790052",
                    longitude="-122.390184",
                    distance="0.5 mi",
                    duration="11 mins",
                    logo_url="https://media.glassdoor.com/sqll/9079/google-squarelogo-1441130773284.png",
                    rating="4.4",
                    industry="Information Technology",
                    glassdoor_url="http://www.glassdoor.com/Reviews/Employee-Review-Google-RVW15868147.htm",
                    station_code="EMBR")

    db.session.add(abc)

    test = Business(business_id=2,
                    name="Test Company",
                    address="653 Harrison St",
                    latitude="37.783158",
                    longitude="-122.396115",
                    distance="0.6 mi",
                    duration="13 mins",
                    logo_url="https://media.glassdoor.com/sqll/659776/udacity-squarelogo-1458083545831.png",
                    rating="4.5",
                    industry="Education",
                    glassdoor_url="https://www.glassdoor.com/Reviews/san-francisco-udacity-reviews-SRCH_IL.0,13_IM759_KE14,21.htm",
                    station_code="MONT")

    db.session.add(test)

    se = Job(job_key="0123456789abcdef",
            title="Software Engineer",
            url="http://www.indeed.com/rc/clk?jk=ac95291e795c6aab",
            date_posted=datetime.datetime(2017, 7, 18, 10, 17, 1),
            duration_posted="13 hours ago",
            business_id=1)

    db.session.add(se)

    se2 = Job(job_key="abcdef0123456789",
            title="Software Engineer, Growth",
            url="http://www.indeed.com/rc/clk?jk=d3850706e430f9f5",
            date_posted=datetime.datetime(2017, 7, 18, 7, 30, 6),
            duration_posted="16 hours ago",
            business_id=2)

    db.session.add(se2)

    test_user = User(user_id=1,
                     email="test@test.com",
                     password="test")

    db.session.add(test_user)

    save = Save(job_key='0123456789abcdef',
                        user_id=1)

    db.session.add(save)

    db.session.commit()


##############################################################################


def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app, db_uri="postgresql:///hbproject"):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
