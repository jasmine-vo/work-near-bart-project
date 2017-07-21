from model import Bart, Business, Job, Save, db
from math import ceil

def get_stations_from_db():
    """Returns query that returns all bart stations including the code, name,
    latitude, and longitude."""

    return db.session.query(Bart.station_code, Bart.station_name, Bart.station_latitude, Bart.station_longitude).all()


def get_current_page_results(job_results, page_num, display_per_page):
    """Returns the job results for the current page"""

    # uses current page number and display per page to slice results for pagination
    return job_results[int(page_num) * display_per_page - display_per_page : int(page_num) * display_per_page]


def get_num_pages(num_results, display_per_page):
    """Calculates the number of page links to create.

    >>> get_num_pages(24, 10)
    3
    """

    # Checks if the total number of job results returned is greater than the
    # number to display per page. If it is, will need more than one page
    if num_results > display_per_page:
        num_pages = int(ceil(num_results / float(display_per_page)))

    else:
        num_pages = 1

    return num_pages

def get_saved_from_db(user_id):
    """Queries the Saved jobs table in the database to get the job ids of all the
    jobs the user saved and converts results into a list."""

    saved = db.session.query(Save.job_key).filter(Save.user_id==user_id).all()
    
    return [save[0] for save in saved]


