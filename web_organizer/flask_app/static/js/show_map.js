function createPolygon(coords) {

  // Construct default polygon.
  var DefaultPolygon = new google.maps.Polygon({
  paths: coords,
  strokeColor: '#FF0000',
  strokeOpacity: 0.8,
  fillColor: '#ffff00',
  fillOpacity: 0.2,
  strokeWeight: 1,
  clickable: true,
  editable: false,
  draggable: false,
  zIndex: 1
  });

  DefaultPolygon.setMap(map);
  polygonArray.push(DefaultPolygon);
}



function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: lat , lng: lng },
    zoom: 11
  });

  if (jQuery.isEmptyObject(coordsDB) == true) {
    coordsDB = DefaultCoords
  }

  createPolygon(coordsDB);

  // Create the DIV to hold the control and call the CenterControl() constructor
  // passing in this DIV.
  var centerControlDiv = document.createElement('div');
  var centerControl = new CenterControl(centerControlDiv, map);

  centerControlDiv.index = 1;
     map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);
}
