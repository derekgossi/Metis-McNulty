var map;

function initmap() {
	// set up the map
	map = new L.Map('map');

	var counties;


	accessToken = 'pk.eyJ1IjoiZ29zc2lkZXJlayIsImEiOiI0V3QxRFBnIn0.labIvjRVeSdi_SVTz8mRWg';
	var mapboxTiles = new L.tileLayer('https://{s}.tiles.mapbox.com/v4/gossiderek.l62iblkf/{z}/{x}/{y}.png?access_token=' + accessToken);

	map.addLayer(mapboxTiles).setView([42.3610, -71.0587], 5); 

                    L.TopoJSON = L.GeoJSON.extend({  
                         addData: function(jsonData) {    
                              if (jsonData.type === "Topology") {
                                   for (key in jsonData.objects) {
                                        geojson = topojson.feature(jsonData, jsonData.objects[key]);
                                        L.GeoJSON.prototype.addData.call(this, geojson);
                                   }
                              }    
                              else {
                                   L.GeoJSON.prototype.addData.call(this, jsonData);
                              }
                         }  
                    });

               var topoLayer = new L.TopoJSON();

               function addTopoData(topoData){  
                         topoLayer.addData(topoData);
                         topoLayer.addTo(map);
                    }

	function style(feature) {
           		return {
                		fillColor: "#FC4E2A",
                		weight: 0.5,
                		opacity: 1,
                		color: 'red',
                		fillOpacity: 0.5
            		};
        	}

        	$.ajax({
  		dataType: "json",
  		async: false,
  		url: "json/us_counties_topo.json",
  		beforeSend: function( data ) {
  			alert("about to send");
            		},
  		success: function( data ) {
  			alert("hello");
  			addTopoData(data);
            		},
            		error: function(jqXHR, textStatus, errorThrown) {
  			alert(textStatus, errorThrown);
		}		
	});	

}          


$(document).ready(function() {

	initmap();

});