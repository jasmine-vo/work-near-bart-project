from sqlalchemy import func
from model import Bart, Business, connect_to_db, db
from server import app


def load_stations():
    """Load location info for each SF Bart station from stations.txt into database"""

    print "Bart Stations"

    Bart.query.delete()

    for row in open('data/stations.txt'):
        row = row.rstrip()
        station_code, name, address, lat_long = row.split('|')

        station = Bart(station_code=station_code,
                       name=name,
                       address=address,
                       lat_long=lat_long)

        db.session.add(station)

    db.session.commit()


def load_businesses():
    """Load businesses and their locations from businesses.txt into database"""

    print "Businesses"

    Business.query.delete()

    for row in open('data/businesses.txt'):
        row = row.rstrip()
        business_id, name, address, lat_long, station_code = row.split('|')

        business = Business(business_id=business_id,
                            name=name,
                            address=address,
                            lat_long=lat_long,
                            station_code=station_code)

        db.session.add(business)

    db.session.commit()


def set_val_business_id():
    """Set value for the next business_id after seeding database"""

    # Get the Max business_id in the database
    result = db.session.query(func.max(Business.business_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('businesses_business_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_stations()
    load_businesses()
    set_val_business_id()
