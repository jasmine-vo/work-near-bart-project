from model import Bart, Business, Job, db
import urllib2
import xmltodict
import os
import requests

bartkey = os.environ['BART_KEY']
indeedkey = os.environ['INDEED_PUBLISHER_ID']


def get_stations():
    """Makes a call to the BART API to get bart stations and their information
    in XML format."""

    url = urllib2.urlopen("http://api.bart.gov/api/stn.aspx?cmd=stns&key={}".format(bartkey))

    data = xmltodict.parse(url.read())

    stations = data.get('root').get('stations').get('station')

    return stations


def call_indeed(start, company):
    """Make a call to the Indeed API to get all job listings for a specific company
    at a start point. Response is in JSON format."""

    params = {'publisher': '{}'.format(indeedkey),
              'v': '2',
              'format': 'json',
              'q': 'company:"{}"'.format(company),
              'l': 'San Francisco, CA',
              'radius': '0',
              'st': 'employer',
              'fromage': 'any',
              'highlight': '0',
              'start': start,
              'limit': '25',
              'userip': '0.0.0.0',
              'useragent': 'Mozilla/%2F4.0%28Firefox%29'
              }

    r = requests.get("http://api.indeed.com/ads/apisearch", params=params)

    return r.json()


def get_job_results(selected_station, title, within_age):
    """Get job results from Indeed based on criteria entered as parameters."""
    
    if selected_station == 'all':
    
        job_results = (db.session.query(Job.url,
                                        Job.title,
                                        Business.name,
                                        Job.date_posted,
                                        Job.duration_posted,
                                        Bart.name)
                        .join(Business)
                        .join(Bart)
                        .filter(Job.title.ilike('%{}%'.format(title)),
                                Job.date_posted > within_age)
                        .order_by(Job.date_posted.desc())
                        .all())

    else:
        
        job_results = (db.session.query(Job.url,
                                        Job.title,
                                        Business.name,
                                        Job.date_posted,
                                        Job.duration_posted,
                                        Bart.name)
                        .join(Business)
                        .join(Bart)
                        .filter(Job.title.ilike('%{}%'.format(title)),
                                Job.date_posted > within_age,
                                Business.station_code==selected_station)
                        .order_by(Job.date_posted.desc())
                        .all())

    return job_results