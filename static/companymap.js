"use strict";

var sanFrancisco = {lat: 37.7598611, lng: -122.4161813};

var map;

function initMap() {

  map = new google.maps.Map(document.getElementById('companymap'), {
      center: sanFrancisco,
      zoom: 13,
      mapTypeControl: false,
      zoomControl: false,
      streetViewControl: false,
  });

  $.get('/results.json', function (job_listings) {

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
    } 
  });    
}





