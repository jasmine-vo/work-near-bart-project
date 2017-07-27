"use strict";

////////////////////////////////////////////////////////////
// Code was pulled from the Google Maps API Documentation //
////////////////////////////////////////////////////////////

// Set a variable to latitude longitude points in San Francisco, CA
var sanFrancisco = {lat: 37.7598611, lng: -122.4161813};

var map;

// Generates a map of San Francisco, CA
function initMap() {
  map = new google.maps.Map(document.getElementById('bartmap'), {
      center: sanFrancisco,
      zoom: 13,
      mapTypeControl: false,
      zoomControl: false,
      streetViewControl: false,
      styles: [
    {
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#AAD4FC"
            }
        ]
    }
],
  });

  // Makes a call to the Flask route to get station info. 
  $.get('/stations.json', function (stations) {

    // Set up empty bounds.
    var bounds = new google.maps.LatLngBounds();

    var station, marker;

    // Loops over the station info to generate markers on the map
    for (var key in stations) {
      station = stations[key];
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(station.stationLatitude, station.stationLongitude),
        map: map,
        label: {
          text: station.stationName,
          // fontWeight: "bold"
        },
        // icon: '/static/img/line-marker.png',
        animation: google.maps.Animation.DROP,
      });
      // Add each marker to bounds 
      bounds.extend(marker.getPosition()); 
    }
    // Fits the map to bounds
    map.fitBounds(bounds);
  });
}
