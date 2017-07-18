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
