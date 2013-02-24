//get location from browser-not required in desktop view
function getLocation() {
    if (navigator.geolocation)
      {
       navigator.geolocation.getCurrentPosition(showPosition,showError);
      }
    else{document.getElementById('mapcontainer').innerHTML="Geolocation is not supported by this browser.";}
      }
  //function showPosition(position) //used when using getLocation()
  //Showing the position in map
  function showPosition()
   {
    //myLatlng = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
    //document.getElementById('latField').value = position.coords.latitude;
    //document.getElementById('lngField').value = position.coords.longitude;
    document.getElementById('latField').value = "8.54385826454";
    document.getElementById('lngField').value = "76.8950002774";
    myLatlng = new google.maps.LatLng("8.54385826454","76.8950002774");//default monvila
    var myOptions = {
      zoom:17,
      center: myLatlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(document.getElementById('mapcontainer'), myOptions);
    
    var marker = new google.maps.Marker({
        position: myLatlng, 
        map: map,
        draggable:true
    });
    google.maps.event.addListener(
        marker,
        'drag',
        function() {
            document.getElementById('latField').value = marker.position.lat();
	    document.getElementById('lngField').value = marker.position.lng();
            
        }
    );
  }

//Error handler
  function showError(error)
    {
     var x = document.getElementById('mapcontainer');
     switch(error.code) 
      {
       case error.PERMISSION_DENIED:
        x.innerHTML="User denied the request for Geolocation."
        break;
       case error.POSITION_UNAVAILABLE:
        x.innerHTML="Location information is unavailable."
        break;
       case error.TIMEOUT:
        x.innerHTML="The request to get user location timed out."
        break;
       case error.UNKNOWN_ERROR:
        x.innerHTML="An unknown error occurred."
        break;
      }
    }
