from sqlalchemy import func
from model import Bart, Business, Job, connect_to_db, db
from functions import get_stations, call_indeed, get_distance, get_company_info
from math import ceil
from server import app
import datetime

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
        
        station_latlong = db.session.query(Bart.latitude, Bart.longitude).filter(Bart.station_code==station_code).first()

        distance_results = get_distance('{},{}'.format(station_latlong[0], station_latlong[1]), '{},{}'.format(latitude, longitude))

        distance = distance_results.get('rows')[0].get('elements')[0].get('distance').get('text')

        duration = distance_results.get('rows')[0].get('elements')[0].get('duration').get('text')

        company_info_results = get_company_info(name)

        if company_info_results is not None:

            print "{} OK".format(name)

            logo_url = company_info_results.get('response').get('employers')[0].get('squareLogo')

            rating = company_info_results.get('response').get('employers')[0].get('overallRating')

            industry = company_info_results.get('response').get('employers')[0].get('sectorName')

            if company_info_results.get('response').get('employers')[0].get('featuredReview'):
                
                glassdoor_url = company_info_results.get('response').get('employers')[0].get('featuredReview').get('attributionURL')

            else:

                glassdoor_url = None

            business = Business(business_id=business_id,
                                name=name,
                                address=address,
                                latitude=latitude,
                                longitude=longitude,
                                distance=distance,
                                duration=duration,
                                logo_url=logo_url,
                                rating=rating,
                                industry=industry,
                                glassdoor_url=glassdoor_url,
                                station_code=station_code)        

        else:

            business = Business(business_id=business_id,
                                name=name,
                                address=address,
                                latitude=latitude,
                                longitude=longitude,
                                distance=distance,
                                duration=duration,
                                station_code=station_code) 

        db.session.add(business)

    db.session.commit()


def load_jobs():
    """Load jobs from Indeed API"""

    print "Jobs"

    Job.query.delete()

    companies = db.session.query(Business.business_id, Business.name).all()
    
    job_results = []

    # makes an Indeed API call for each company in database.
    for company in companies:

        indeed_request = call_indeed(0, company[1])

        results = indeed_request.get('results')

        # if there are results, adds business_id, appends to job_results list
        if results:
            for job in results:
                job['business_id'] = company[0]
                job_results.append(job)

        # gets total number of jobs opened under the company
        num_jobs = indeed_request.get('totalResults')

        # divides total number of jobs divided max result returned (25) to get 
        # number of times to repeat API call
        repeat = int(ceil(num_jobs / 25.0)) - 1

        if repeat > 1:
            for n in range(1, repeat + 1):
                start = n * 25
                indeed_request = call_indeed(start, company[1])
                results = indeed_request.get('results')

                if results:
                    for job in results:
                        job['business_id'] = company[0]
                        job_results.append(job)
    job_id = 0

    for result in job_results:
        job_id += 1
        url = 'http://www.indeed.com/rc/clk?jk={}'.format(result.get('jobkey'))
        title = result.get('jobtitle')
        date_posted = datetime.datetime.strptime(result.get('date'), '%a, %d %b %Y %H:%M:%S %Z')
        duration_posted = result.get('formattedRelativeTime')
        business_id = result.get('business_id')

        job = Job(job_id=job_id,
                  url=url,
                  title=title,
                  date_posted=date_posted,
                  duration_posted=duration_posted,
                  business_id=business_id)

        db.session.add(job)

    db.session.commit()


def load_users():
    """Load users."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    demo = User(user_id=1,
                   email='demo@demo.com',
                   password='123')

    # We need to add to the session or it won't ever be stored
    db.session.add(demo)

    # Once we're done, we should commit our work
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
    load_jobs()
    set_val_business_id()
