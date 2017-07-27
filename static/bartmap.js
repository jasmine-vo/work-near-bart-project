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

  $.get('/stations.json', function (stations) {

    // set up empty bounds
    var bounds = new google.maps.LatLngBounds();

    var station, marker;

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
      // add each marker to bounds 
      bounds.extend(marker.getPosition()); 
    }
    // fit map to bounds
    map.fitBounds(bounds);
  });
}
