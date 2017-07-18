"use strict";

var sanFrancisco = {lat: 37.7598611, lng: -122.4161813};

var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('bartmap'), {
      center: sanFrancisco,
      zoom: 13,
      mapTypeControl: false,
      zoomControl: false,
      streetViewControl: false,
  });

  $.get('/stations.json', function (stations) {

    var station, marker;

    for (var key in stations) {
      station = stations[key];
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(station.stationLatitude, station.stationLongitude),
        map: map,
        label: station.stationName,
        animation: google.maps.Animation.DROP,
      });
    }
  });
}
