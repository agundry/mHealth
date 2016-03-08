$(document).ready( function() {
    $("#infectionButton").click(function(e) {
        var email = $("#emailAddress").val();
        console.log(email);
        $.ajax({
            url: "http://127.0.0.1:8000/searchConnections?email="+email,
            success : function(data) {
                console.log(data);
            }
        });
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

function submitInfection() {
    email = $('#emailAddress').val();
    infection = $('#infectionName').val();
    if (email = '') {
        alert("Please enter in a valid email address")
    }
    else if (infectionName = '') {
        alert("Please enter a valid infection")
    }
    else {
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:8000/searchConnections?email="+email+"&infection="+infection,
            success : function(data) {
                console.log(data);
            }
        });
    }
}