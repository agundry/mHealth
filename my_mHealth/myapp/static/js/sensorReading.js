var pics = {"abgundry@u.northwestern.edu":"austin",
                            "sachinlal2016@u.northwestern.edu":"sachin",
                            "doge@gmail.com":"doge"};

$(document).ready( function() {
    $("#infectionButton").click(function(e) {
        var email = $("#emailAddress").val();
        console.log(email);
        $.ajax({
            url: "http://192.168.1.117:8000/searchConnections?email="+email,
            success : function(data) {
                var pics = {"abgundry@gmail.com":"austin",
                                            "sachinlal2016@u.northwestern.edu":"sachin",
                                            "doge@gmail.com":"doge"};
                var static_dir = "/Users/Austin/Documents/Northwestern/mHealth/my_mHealth/myapp/static/img/";
                $("#results").empty();
                console.log(data);
                var results = JSON.parse(data);
                var keys = Object.keys(results);
                var statements = [];
                $("#results").append("<div class=\"row\"><div class=\"col-lg-5 col-lg-offset-4\">" +
                                      "<h2>Infection Report requested for:</h2>"+
                                      "</div></div>"+
                                      "<div class=\"row\"><div class=\"col-lg-2 col-lg-offset-4\"><img src=\""+static_dir+pics[email]+".jpg\" class=\"img-circle\">" +
                                    "</div><div class=\"col-lg-4\"><h3>"+email+"</h3></div></div>"+
                                    "<div class=\"row\"><div class=\"col-lg-5 col-lg-offset-4\"><h4>The following users have come into contact with the infected recently:</h4></div></div>");

                for (i = 0; i < keys.length; i++){
                    statements = [];
                    for (j = 0; j < results[keys[i]].length; j++) {
                        statements.push(results[keys[i]][j][0]+ " aggregate seconds at beacon " + results[keys[i]][j][1]);
                    }
                    $("#results").append("<ul class=\"person\">" +
                                          "<li style=\"list-style-type: none;\" >"+
                                            "<div class=\"col-lg-2\">" +
                                              "<img src=\""+static_dir+pics[keys[i]]+".jpg\" class=\"img-circle\">" +
                                            "</div>"+
                                            "<div class=\"col-lg-9 col-lg-offset-1\">" +
                                              "<h2>"+keys[i]+"</h2>" +
                                              "<p>"+statements.join()+"</p>" +
                                            "</div>"+
                                          "</li>"+
                                        "</ul>");
                    $("#results").append("<ul class=\"person\">" +
                                          "<li style=\"list-style-type: none;\" >"+
                                            "<div class=\"col-lg-2\">" +
                                              "<img src=\""+static_dir+pics[keys[i]]+".jpg\" class=\"img-circle\">" +
                                            "</div>"+
                                            "<div class=\"col-lg-9 col-lg-offset-1\">" +
                                              "<h2>"+keys[i]+"</h2>" +
                                              "<p>"+statements.join()+"</p>" +
                                            "</div>"+
                                          "</li>"+
                                        "</ul>");
                }
            }
        });
        return false;
    })
});


//function updatePage() {
//    $.ajax({
//        url: "http://127.0.0.1:8000/update",
//        success : function(data) {
//            console.log(data);
//            if (data == "Hello") {
//                $('body').css("background-image", 'url("https://media.giphy.com/media/Qbyo7WjdZKyNq/giphy.gif")');
//            }
//            else {
//                $('body').css("background-image", 'url("https://media.giphy.com/media/WlBUAWG03Zic8/giphy.gif")');
//            }
//        }
//    });
//    setTimeout(function(){updatePage();},1000);
//}

//function submitInfection() {
//    email = $('#emailAddress').val();
//    infection = $('#infectionName').val();
//    if (email = '') {
//        alert("Please enter in a valid email address")
//    }
//    else if (infectionName = '') {
//        alert("Please enter a valid infection")
//    }
//    else {
//        $.ajax({
//            type: "GET",
//            url: "http://192.168.1.117:8000/searchConnections?email="+email+"&infection="+infection,
//            success : function(data) {
//                console.log(data);
//            }
//        });
//    }
//}