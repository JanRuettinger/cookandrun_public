function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lat , lng: lng },
        zoom: 11
        });

    var teams = [];
    for (index = 0; index < teams_long.length; ++index) {
        teams.push([teams_long[index], teams_long[index+1], teams_long[index+2], teams_long[index+3]]);
    }

    function pinSymbol(color_num) {
        colors = ['#123','#222','#FF1','#91F'];
        colors = ['#FF2D55', '#007AFF', '#4CD964', '#FEE94E', '#5AC8FA', '#808080','#159588', '#9A5CB4', '#159588'];
        return {
            path: 'M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z M -2,-30 a 2,2 0 1,1 4,0 2,2 0 1,1 -4,0',
            fillColor: colors[color_num],
            fillOpacity: 1,
            strokeColor: '#000',
            strokeWeight: 2,
            scale: 1,
        };
    }
    
    teams.forEach(function(team) {
    var myLatLng = {lat: parseFloat(team[1]), lng: parseFloat(team[2])};
    var marker = new google.maps.Marker({
                  position: myLatLng,
                  map: map,
                  icon: pinSymbol(team[3]),
                });
    console.log(team[0]);
    });
}
