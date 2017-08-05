# Work Near BART

Need a job you can ride BART to? This app can help you search for a job within walking distance (~15 mins) to a station in San Francisco. Users can search by job title, and filter by destination and days posted. The app will return a list of jobs from Indeed as well as the closest BART station and estimated walking time. If available, the Glassdoor rating for the company is provided. If a starting point is selected, the fare amount is calculated using the BART API. If logged in, the user can save a list of jobs they are interested in. The Google Map on the results page will generate markers for all the companies on the current page. If the user clicks on a company's marker, the map will show the walking directions from the station.

## Technology Stack

Python, JavaScript, AJAX, JSON, HTML, CSS, Flask, jQuery, Bootstrap,  Jinja, PostgreSQL, Unittest.

## APIs Used

SF Data, Google Maps, Google Distance Matrix, Indeed, BART, Glassdoor

### TO DO:

Short term:
- Add more tests
- Add warning message when user deletes a job from their saved jobs list
- Finish styling Login and Register pages

Long term:
- Change data set up process, looking into Google Places API
- Expand beyond San Francisco (Oakland next?)

## DEMO

![alt tag](/static/img/demo1.gif)

![alt tag](/static/img/demo2.gif)

![alt tag](/static/img/demo3.gif)