   
$(document).ready(function() {

        $('#test_button').click(function() {
                $.ajax({
                        type: "post",
                        datatype:"text",
                        async: false,
                        url: "python/python_http.py",
                        data: { 'age_range' : [20,32], 'income_range' : [65000, 95000] },
                        beforeSend: function( data ) {
                                alert("about to send");
                        },
                        success: function( data ) {
                                alert(data);
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                                alert(textStatus);
                                alert(errorThrown);
                        }   
                }); 
        });

      // $.ajax({
      //     dataType: "json",
      //     async: false,
      //     url: "json/us_counties_topo.json",
      //     beforeSend: function( data ) {
      //         alert("about to send");
      //     },
      //       success: function( data ) {
      //         alert("hello");
      //       },
      //       error: function(jqXHR, textStatus, errorThrown) {
      //         alert(textStatus, errorThrown);
      //       }   
      //   }); 

});