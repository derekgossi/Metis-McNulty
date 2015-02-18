
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
        $('#test_button').click(function() {
                $.ajax({
                        type: "post",
                        datatype:"text",
                        async: false,
                        url: "python/get_map_data.py",
                        data: { 'age_range' : [20,32], 'income_range' : [65000, 95000] },
                        beforeSend: function( data ) {
                                showMapSpinner();
                                alert("why");
                        },
                        success: function( data ) {
                                alert(data);
                                $("#map_canvas").empty()

                                queue()
                                        .defer(d3.json, "json/us_counties_topo_mbo.json")
                                        .defer(d3.tsv, "csv/mapping_data_live.tsv", function(d) { rateById.set(d.id, +d.rate); })
                                        .await(ready);

                                hideMapSpinner();
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                                alert(textStatus);
                                alert(errorThrown);
                        }   
                }); 
        });
        
        // D3 sliders
        d3.select("body")
                .select("#age_slider")
                .call(d3.slider()
                .axis(true)
                .min(15)
                .max(85)
                .step(5));

        d3.select("body")
                .select("#income_slider")
                .call(d3.slider()
                .axis(true)
                .min(0)
                .max(200000)
                .step(5));



        // D3 mapping
        var width = 960, height = 600;

        var rateById = d3.map();

        var quantize = d3.scale.quantize()
                .domain([0, .2])
                .range(d3.range(9).map(function(i) { return "q" + i + "-20"; }));

        var projection = d3.geo.albersUsa()
                .scale(1280)
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

