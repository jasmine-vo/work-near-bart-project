from sqlalchemy import func
from model import Bart, Business, connect_to_db, db
from server import app


def load_stations():
    """Makes a call to BART API to get all SF station locations and loads information 
    into database"""

    print "Bart Stations"

    Bart.query.delete()

    stations = get_stations()

    sf_stations = [s for s in stations if s.get('city') == 'San Francisco']

    for station in sf_stations:
        station_code = station.get('abbr')
        name = station.get('name')
        address = station.get('address')
        city = station.get('city')
        state = station.get('state')
        zipcode = station.get('zipcode')
        latitude = station.get('gtfs_latitude')
        longitude = station.get('gtfs_longitude')

        station = Bart(station_code=station_code,
                       name=name,
                       address=address,
                       city=city,
                       state=state,
                       zipcode=zipcode,
                       latitude=latitude,
                       longitude=longitude)

        db.session.add(station)

    db.session.commit()


def load_businesses():
    """Load businesses and their locations from businesses.txt into database"""

    print "Businesses"

    Business.query.delete()

    for row in open('data/businesses.txt'):
        row = row.rstrip()
        business_id, name, address, latitude, longitude, station_code = row.split('|')

        business = Business(business_id=business_id,
                            name=name,
                            address=address,
                            latitude=latitude,
                            longitude=longitude,
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
