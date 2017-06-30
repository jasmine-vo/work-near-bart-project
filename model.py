from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bart(db.Model):
    """Bart stations."""

    __tablename__ = "stations"

    station_code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    lat_long = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Bart station_code=%s name=%s address=%s lat_long=%s>"
        return s % (self.station_code, self.name, self.address, self.lat_long)


class Business(db.Model):
    """Business locations."""

    __tablename__ = "businesses"

    business_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    lat_long = db.Column(db.String(30), nullable=False)
    station_code = db.Column(db.String(3),
                             db.ForeignKey('stations.station_code'),
                             nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Business business_id=%s name=%s address=%s lat_long=%s station_code=%s>"
        return s % (self.business_id,
                    self.name,
                    self.address,
                    self.lat_long,
                    self.station_code)


# class Job(db.Model):
#     """Job details."""

#     __tablename__ = "jobs"

#     job_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     title = db.Column(db.String(50), nullable=False)
#     business_id = db.Column(db.Integer,
#                             db.ForeignKey("business.business_id"),
#                             nullable=False)

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         s = "<Job job_id=%s name=%s title=%s business_id=%s>"
#         return s % (self.job_id, self.name, self.title, self.business_id)


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



