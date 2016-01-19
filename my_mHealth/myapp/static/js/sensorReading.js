$(document).ready( function() {
	updatePage();
});


function updatePage() {
    $.ajax({
        url: "http://192.168.1.124:8000/update",
        success : function(data) {
            console.log(data);
            if (data == "Hello") {
                $('body').css("background-image", 'url("https://media.giphy.com/media/Qbyo7WjdZKyNq/giphy.gif")');
            }
            else {
                $('body').css("background-image", 'url("https://media.giphy.com/media/WlBUAWG03Zic8/giphy.gif")');
            }
        }
    });
    setTimeout(function(){updatePage();},1000);
}
