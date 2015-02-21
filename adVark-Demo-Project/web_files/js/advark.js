
function showMapSpinner() {
        $('#map_spinner').show();
}

function hideMapSpinner() {
        $('#map_spinner').hide();
}


// On document ready
$(document).ready(function() {
        // Hidden elements
         $('#map_spinner').hide();

        // Ajax call to get joint distributions
        $('#new_map_button').click(function() {
                var age_low = $( "#age_slider" ).slider( "values", 0 );
                var age_high = $( "#age_slider" ).slider( "values", 1 );
                var income_low = $( "#income_slider" ).slider( "values", 0 );
                var income_high = $( "#income_slider" ).slider( "values", 1 );

                $.ajax({
                        type: "post",
                        datatype:"text",
                        async: true,
                        url: "python/get_map_data.py",
                        data: { 'age_range' : [age_low,age_high], 'income_range' : [income_low, income_high] },
                        beforeSend: function( data ) {
                                showMapSpinner();
                                $('#new_map_button').text("Loading new data...").append("<div id=\"map_spinner\"></div>");
                        },
                        success: function( data ) {
                                $("#map_canvas").empty()

                                queue()
                                        .defer(d3.json, "json/us_counties_topo_mbo.json")
                                        .defer(d3.tsv, "csv/mapping_data_live.tsv", function(d) { rateById.set(d.id, +d.rate); })
                                        .await(ready);

                                hideMapSpinner();

                                $('#new_map_button').text("Refresh");
                                var percent_data = parseFloat(data) * 100;
                                $('#max_scale_text').text(percent_data.toFixed(1) + "%");
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                                alert(textStatus);
                                alert(errorThrown);
                        }   
                }); 
        });
        
        $(function() {
                $( "#age_slider" ).slider({
                        range: true,
                        min: 15,
                        max: 85,
                        values: [ 25, 35 ],
                        slide: function( event, ui ) {
                                $( "#age_amount" ).val( "" + ui.values[ 0 ] + " - " + ui.values[ 1 ] );
                        }
                });

                $( "#income_slider" ).slider({
                        range: true,
                        min: 0,
                        max: 200,
                        values: [ 0, 50 ],
                        slide: function( event, ui ) {
                                $( "#income_amount" ).val( "" + ui.values[ 0 ] + "k - " + ui.values[ 1 ] + "k" );
                        }
                });

                $( "#age_amount" ).val( "" + $( "#age_slider" ).slider( "values", 0 ) +
                        " - " + $( "#age_slider" ).slider( "values", 1 ) );

                $( "#income_amount" ).val( "" + $( "#income_slider" ).slider( "values", 0 ) +
                        "k - " + $( "#income_slider" ).slider( "values", 1 ) + "k" );
        });



        // D3 mapping
        var width = 700, height = 500;

        var rateById = d3.map();

        var quantize = d3.scale.quantize()
                .domain([0, 1])
                .range(d3.range(20).map(function(i) { return "q" + i + "-20"; }));

        var projection = d3.geo.albersUsa()
                .scale(900)
                .translate([width / 2, height / 2]);

        var path = d3.geo.path()
                .projection(projection);

        function zoom() {
                svg.select("g")
                .attr("transform", "translate("
                        + d3.event.translate
                        + ")scale(" + d3.event.scale + ")");
        }

        function zoomStates() {
                svg.select(".states")
                .attr("transform", "translate("
                        + d3.event.translate
                        + ")scale(" + d3.event.scale + ")");
        }

        var svg = d3.select("body").select("#map_canvas")
                .attr("width", width)
                .attr("height", height);

        queue()
                .defer(d3.json, "json/us_counties_topo_mbo.json")
                .defer(d3.tsv, "csv/unemployment.tsv", function(d) { rateById.set(d.id, +d.rate); })
                .await(ready);

        function ready(error, us) {
                svg.append("g")
                        .attr("class", "counties")
                        .call(d3.behavior.zoom()
                        .scaleExtent([1, 10])
                        .on("zoom", zoom))
                        .selectAll("path")
                        .data(topojson.feature(us, us.objects.counties).features)
                        .enter().append("path")
                        .attr("class", function(d) { return quantize(rateById.get(d.id)); })
                        .attr("d", path)
                        .attr("id", function(d) {return d.id} );

                svg.select("g")
                        .append("path")
                        .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
                        .attr("class", "states")
                        .attr("d", path);
        }

        d3.select(self.frameElement).style("height", height + "px");

});

