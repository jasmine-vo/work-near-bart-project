"use strict";

////////////////////////////////////////////////////////////
// Code was pulled from the Google Maps API Documentation //
////////////////////////////////////////////////////////////

var sanFrancisco = {lat: 37.7598611, lng: -122.4161813};

var map;

// To stylize the reset button on the map and add event listener.
function CenterControl(controlDiv, map) {

  // Set CSS for the control border.
  var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = '#0a96d4';
    // controlUI.style.border = '1px solid #fff';
    // controlUI.style.borderRadius = '0x';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginBottom = '22px';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Click to recenter the map';
    controlDiv.appendChild(controlUI);

  // Set CSS for the control interior.
  var controlText = document.createElement('div');
    controlText.style.color = '#fff';
    controlText.style.fontFamily = 'Arial,sans-serif';
    controlText.style.fontSize = '14px';
    controlText.style.lineHeight = '25px';
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

    // Loops over the job listings to generate markers for each company on the
    // current page
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
      
      // Displays the walking directions on the map, function is ran when a
      // marker is clicked.
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

      // Add event listener to markers, and runs the calculateAndDisplayRoute
      // function when clicked.
      marker.addListener('click', function (evt) {
        var position = this.position
        var stationPosition = this.stationPosition

        calculateAndDisplayRoute(directionsService, directionsDisplay, position, stationPosition);
      });

      // Add each marker to bounds 
      bounds.extend(marker.getPosition());
    }
    // Fit map to bounds
    map.fitBounds(bounds);
  });    
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// The below code adds event listener to the window.  When the page is                                         //
// scrolled down, the map fill be fixed to the top of the page.  I used code                                   //
// from answer on Stack Overflow, link below:                                                                  //
// https://stackoverflow.com/questions/36276293/fix-div-when-position-reaches-85px-from-top-of-window-on-scroll//
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////


$(function(){
  // Get the position of the company map div
  var fixedToTop = $('#companymap').offset().top;

  // Get the position of the media on left side of page
  var mediaLeft = $('.media-wrapper').offset().left;
  var mediaTop = $('.media-wrapper').offset().top;

  // Add event listener to window scroll.  When user scrolls up/down, the CSS 
  // of the map's div changes.
  $(window).scroll(function(){
    if( $(window).scrollTop() > fixedToTop) {
            $('#companymap').css({position: 'fixed',
                                  top: '10px',
                                  right: mediaLeft + 'px'});  
    } else {
            $('#companymap').css({height: '400px',
                                  width: '350px',
                                  top: '',
                                  // right: mediaLeft + 'px'
                                });
    }
  });
});

// $(function(){
//   // Get the element company map div
//   var companyMap = $('#companymap');

//   // Get window width
//   var windowWidth = $( window ).width();

//   if (windowWidth < 770) {
//     companyMap.hide();
//   } else {
//     companyMap.show();
//   }
// });








