from model import Bart, db, connect_to_db
from flask import Flask
import requests
import urllib2
import xmltodict
import os

app = Flask(__name__)

bartkey = os.environ['BART_KEY']

def get_stations():
    """Makes a call to the BART API to get bart stations and their information
    in XML format."""

    url = urllib2.urlopen("http://api.bart.gov/api/stn.aspx?cmd=stns&key={}".format(bartkey))

    data = xmltodict.parse(url.read())

    stations = data.get('root').get('stations').get('station')

    return stations



if __name__ == "__main__":
    
    app = Flask(__name__)
    connect_to_db(app)
