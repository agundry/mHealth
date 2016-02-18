$(document).ready( function() {
	updatePage();
});


function updatePage() {
    $.ajax({
        url: "http://10.105.135.121:8000/update",
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
