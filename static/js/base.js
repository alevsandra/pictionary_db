//setting countdown
let seconds = 60;
//countdown function
var x = setInterval(function onTimer() {
    //updating clock
    if(seconds === 60) document.getElementById('count_down').innerHTML = "1 : 00";
    else document.getElementById('count_down').innerHTML = 0 + " : " + seconds;
    seconds--;
    //when countdown ends
    if (seconds < 0) {
        clearInterval(x);
        next_page();
    }
}, 1000);

//redirecting to the next page function
function next_page() {
    //creating csrf token
    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    save();

    //sending post request to delete from temp model
    $.ajax({
        type: 'POST',
        url: deletion_link,
        headers: {'X-CSRFToken': csrf_token},
    }).then(() => {
            if (model_length > 1)
                location.href = new_picture;
            else
                location.href = result_page;
        }, () => {
            if (model_length > 1)
                location.href = new_picture;
            else
                location.href = result_page;
        }
    );

    //redirect link to the next page
    // if (model_length > 1) location.href = new_picture;
    // else location.href = result_page;
}

//temp model creation
function random_temp_category() {
    $.post(random_link, {}, function myCallback(data) {
        location.href = first_category.replace('1', data.pid);
    });
}

//initializing canvas
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext("2d");

//function to set up brush color
function color(color_value) {
        ctx.strokeStyle = color_value;
        ctx.fillStyle = color_value;
}

window.addEventListener('load', () => {

    //canvas size
    ctx.canvas.height = 0.65 * window.innerHeight;
    //mobile
    if (window.innerHeight > window.innerWidth) ctx.canvas.width = 0.90 * window.innerWidth;
    //desktop
    else ctx.canvas.width = 0.60 * window.innerWidth;

    let painting = false;
    let brushSize = 5;
    let brushPos = {x: 0, y: 0};


    function getBrushPos(canvasCtx, e) {
        let x = e.type.includes("touch") ?
            e.touches[0].clientX : e.clientX;
        let y = e.type.includes("touch") ?
            e.touches[0].clientY : e.clientY;
        let rect = canvasCtx.getBoundingClientRect();
        return {
            x: x - rect.left,
            y: y - rect.top
        };
    }

    //drawing
    function start(e) {
        painting = true;
        ctx.beginPath();
        brushPos = getBrushPos(canvas, e);
        ctx.moveTo(brushPos.x, brushPos.y);
        draw(e);
        e.preventDefault();
    }

    function draw(e) {
        if (!painting) return;
        ctx.lineWidth = brushSize;
        ctx.lineCap = 'round';
        brushPos = getBrushPos(canvas, e);
        ctx.lineTo(brushPos.x, brushPos.y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(brushPos.x, brushPos.y);
        e.preventDefault();
    }

    function end(e) {
        ctx.closePath();
        painting = false;
        e.preventDefault();
    }

    canvas.addEventListener('mousedown', start);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', end);
    canvas.addEventListener('mouseout', end);
    canvas.addEventListener('touchstart', start);
    canvas.addEventListener('touchmove', draw);
    canvas.addEventListener('touchend', draw);


    document.addEventListener('click', (e) => {
        let x = e.target
        if (x.id === 'reset') ctx.clearRect(0, 0, canvas.width, canvas.height);
    });

});
function save (){
    var image = canvas.toDataURL("image/png");

    $.post(save_link, {
        category: category_name,
        save_image: image,
    });

}