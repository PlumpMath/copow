//
// copow javascript utility functions
// ** did never expect I make one of those, ever ;)
//
// khz June / 2014
// www.pythononwheels.org
//
var del;
del = function(target_url) {
        console.log("delete clicked", target_url);
        console.log("url: " + target_url)
        $.ajax( 
            {
                type: 'DELETE',
                url: target_url,
                data: "",
                contentType: "application/json",
                dataType: "json"
            }
        )
        .done(function(msg) {
            //alert( "success" );
            console.log(msg);
            //var payload = JSON.parse(msg.responseText);
            console.log(msg["data"]);
            $("#flash_message").text("sucess:" + msg["data"]);
            $("#flash_message_div").attr("class",
                "alert alert-success alert-dismissible"
             );
            $("#flash_message_div").show();

        })
        .fail(function( msg ) {
            //alert( "error" );
            console.log(msg);
            var payload = JSON.parse(msg.responseText);
            console.log(payload["data"]);
            $("#flash_message").text("Error :" + payload["data"]);
             $("#flash_message_div").attr("class",
                "alert alert-danger alert-dismissible"
             )
            $("#flash_message_div").show();
        })
        .always(function() {
            //alert( "complete" );
            console.log("complete")
        });
    };