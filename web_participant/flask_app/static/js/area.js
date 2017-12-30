var map;
var polygonArray = [];
//Define polygon

var DefaultCoords = [
  {lat: lat + 0.02, lng: lng + 0.02},
  {lat: lat + 0.02, lng: lng - 0.02},
  {lat: lat - 0.02, lng: lng - 0.02},
  {lat: lat - 0.02, lng: lng + 0.02}];



$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
      }
  }
})

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
 controlUI.title = 'Click to get your default area';
 controlDiv.appendChild(controlUI);

 // Set CSS for the control interior.
  var controlText = document.createElement('div');
  controlText.style.color = 'rgb(25,25,25)';
  controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
  controlText.style.fontSize = '16px';
  controlText.style.lineHeight = '38px';
  controlText.style.paddingLeft = '5px';
  controlText.style.paddingRight = '5px';
  controlText.innerHTML = 'Reset area';
  controlUI.appendChild(controlText);

  // Setup the click event listeners: simply set the map to Chicago.
  controlUI.addEventListener('click', resetPolygon)
}

function resetPolygon() {

  // remove old polygon
  for (i in polygonArray) {
    polygonArray[i].setMap(null);
  }

  createPolygon(DefaultCoords);
}

var debounce = function(func, delay) {
  var inDebounce = undefined;
  return function() {
    var context = this,
          args = arguments;
    clearTimeout(inDebounce);
    return inDebounce = setTimeout(function() {
      return func.apply(context, args);
    }, delay);
  }
}

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
  editable: true,
  draggable: true,
  zIndex: 1
  });

  DefaultPolygon.setMap(map);
  polygonArray.push(DefaultPolygon);

  SendPolygonToBackEnd(DefaultPolygon);

  DefaultPolygon.getPaths().forEach(function(path, index){

    google.maps.event.addListener(path, 'insert_at', debounce(function(){
      SendPolygonToBackEnd(DefaultPolygon); }, 250));

    google.maps.event.addListener(path, 'remove_at', debounce(function(){
      SendPolygonToBackEnd(DefaultPolygon); }, 250));

    google.maps.event.addListener(path, 'set_at', debounce(function(){
      SendPolygonToBackEnd(DefaultPolygon); }, 250));

  });

  google.maps.event.addListener(DefaultPolygon, 'dragend', debounce(function(){ SendPolygonToBackEnd(DefaultPolygon); }, 250));

}

function SendPolygonToBackEnd(polygon) {
  var vertices = polygon.getPath();
  var coords = []

  for (var i =0; i < vertices.getLength(); i++) {
    var xy = vertices.getAt(i);
    coords.push(
      {lat: xy.lat(), lng: xy.lng()})
  }
  console.log(coords)

  $.ajax({
    type: "POST",
    url: "/area",
    data: JSON.stringify(coords),
    contentType: "application/json",
    dataType: "json",
    success: function(data){},
    failure: function(errMsg) {}
  });
}

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: lat , lng: lng },
    zoom: 11
  });

 // var coordsDB = {{ db_polygon|safe }};

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

