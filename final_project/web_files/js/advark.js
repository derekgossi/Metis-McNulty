var map;

function initmap() {
	// set up the map
	map = new L.Map('map');

	var counties;

	accessToken = 'pk.eyJ1IjoiZ29zc2lkZXJlayIsImEiOiI0V3QxRFBnIn0.labIvjRVeSdi_SVTz8mRWg';
	var mapboxTiles = new L.tileLayer('https://{s}.tiles.mapbox.com/v4/gossiderek.l62iblkf/{z}/{x}/{y}.png?access_token=' + accessToken);

	map.addLayer(mapboxTiles).setView([42.3610, -71.0587], 5);	

	function style(feature) {
           		return {
                		fillColor: "#FC4E2A",
                		weight: 0.5,
                		opacity: 1,
                		color: 'black',
                		fillOpacity: 0.5
            		};
        	}

        	$.ajax({
  		dataType: "json",
  		async: false,
  		url: "json/us_counties.json",
  		beforeSend: function( data ) {
  			alert("about to send");
            		},
  		success: function( data ) {
  			alert("hello");
  			geojson = L.geoJson(data, {
                			style: style
            			}).addTo(map);
            		},
            		error: function(jqXHR, textStatus, errorThrown) {
  			alert(textStatus, errorThrown);
		}		
	});	

}          


$(document).ready(function() {

	initmap();

});