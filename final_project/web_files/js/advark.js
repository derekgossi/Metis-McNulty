var map;

function initmap() {
	// set up the map
	map = new L.Map('map');

	accessToken = 'pk.eyJ1IjoiZ29zc2lkZXJlayIsImEiOiI0V3QxRFBnIn0.labIvjRVeSdi_SVTz8mRWg';
	var mapboxTiles = new L.tileLayer('https://{s}.tiles.mapbox.com/v4/gossiderek.l62iblkf/{z}/{x}/{y}.png?access_token=' + accessToken);

	map.addLayer(mapboxTiles).setView([42.3610, -71.0587], 15);	
}          


$(document).ready(function() {
    
	initmap();

});