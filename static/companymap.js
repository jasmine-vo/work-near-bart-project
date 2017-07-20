"use strict";

var sanFrancisco = {lat: 37.7598611, lng: -122.4161813};

var map;

// To stylize the reset button on the map and add event listener.
function CenterControl(controlDiv, map) {

  // Set CSS for the control border.
  var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.border = '2px solid #fff';
    controlUI.style.borderRadius = '3px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginBottom = '22px';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Click to recenter the map';
    controlDiv.appendChild(controlUI);

  // Set CSS for the control interior.
  var controlText = document.createElement('div');
    controlText.style.color = 'rgb(25,25,25)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.lineHeight = '38px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';
    controlText.innerHTML = 'Reset Map';
    controlUI.appendChild(controlText);

  // Runs initMap when reset button is clicked.
  controlUI.addEventListener('click', function() {
    initMap();
  });
}

function initMap() {

  // Creates new map
  map = new google.maps.Map(document.getElementById('companymap'), {
      center: sanFrancisco,
      zoom: 13,
      mapTypeControl: false,
      zoomControl: false,
      streetViewControl: false,
  });

  // Create div element for reset button
  var centerControlDiv = document.createElement('div');
  var centerControl = new CenterControl(centerControlDiv, map);

  // Set reset button on map
  centerControlDiv.index = 1;
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);

  $.get('/results.json', function (job_listings) {

    // set up empty bounds
    var bounds = new google.maps.LatLngBounds();

    var job, marker, jobLatitude, jobLongitude;
    console.log(job_listings);
    for (var key in job_listings) {
      job = job_listings[key];
      jobLatitude = parseFloat(job.jobLatitude);
      jobLongitude = parseFloat(job.jobLongitude);

      marker = new google.maps.Marker({
        position: new google.maps.LatLng(jobLatitude, jobLongitude),
        map: map,
        label: job.jobCompany,
        animation: google.maps.Animation.DROP,
        stationName: job.stationName,
        stationPosition: {lat: parseFloat(job.stationLatitude), lng: parseFloat(job.stationLongitude)}
      }); 
    
      function calculateAndDisplayRoute(directionsService, directionsDisplay, position, stationPosition) {
        directionsService.route({
        origin: stationPosition,
        destination: position,
        travelMode: google.maps.TravelMode['WALKING']
        }, function(response, status) {
          if (status == 'OK') {
            directionsDisplay.setDirections(response);
          } else {
          window.alert('Directions request failed due to ' + status);
          }
        });
      }

      var directionsService = new google.maps.DirectionsService;
      var directionsDisplay = new google.maps.DirectionsRenderer;
      directionsDisplay.setMap(map);

      marker.addListener('click', function (evt) {
        var position = this.position
        var stationPosition = this.stationPosition

        calculateAndDisplayRoute(directionsService, directionsDisplay, position, stationPosition);
      });

      // add each marker to bounds 
      bounds.extend(marker.getPosition());
    }
    // fit map to bounds
    map.fitBounds(bounds);
  });    
}







