let seconds = 60;
var x = setInterval(function onTimer() {
    document.getElementById('count_down').innerHTML = 0 + " : " + seconds;
    seconds--;
    if (seconds < 0) {
        clearInterval(x);
        document.getElementById("delete_form").submit();
        location.href=new_picture;
    } else {

        document.getElementById("count_down").innerHTML = 0 + " : " + seconds;
    }
}, 1000);

