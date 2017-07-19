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

    var job, marker, latitude, longitude;

    for (var key in job_listings) {
      job = job_listings[key];
      latitude = parseFloat(job.jobLatitude)
      longitude = parseFloat(job.jobLongitude)

      marker = new google.maps.Marker({
        position: new google.maps.LatLng(latitude, longitude),
        map: map,
        label: job.jobCompany,
        animation: google.maps.Animation.DROP,
      });
    }
  });
}