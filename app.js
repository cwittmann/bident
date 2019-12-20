// Set constraints for the video stream
var constraints = { video: { facingMode: "user" }, audio: false };// Define constants

const cameraView = document.querySelector("#camera--view"),
    cameraOutput = document.querySelector("#camera--output"),
    cameraSensor = document.querySelector("#camera--sensor"),
    cameraTrigger = document.querySelector("#camera--trigger")// Access the device camera and stream to cameraView

function cameraStart() {
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function(stream) {
        track = stream.getTracks()[0];
        cameraView.srcObject = stream;
    })
    .catch(function(error) {
        console.error("Oops. Something is broken.", error);
    });
}

function postData(input) {    
    $.ajax({
        type: "POST",
        url: "http://cwittmann.pythonanywhere.com/",
        data: { param: input },
        success: callbackFunc,
        error: errorFunc
    });

    fetch("http://cwittmann.pythonanywhere.com/", { method: 'POST', body: input, mode: 'cors' })
        .then(function(data) {
            console.log(data);
        })
        .catch(function(error) {
            alert(error);
            console.log(error);    
        });
}

function callbackFunc(response) {
    // do something with the response    
    alert(response.statusText);
}

function errorFunc(response) {
    // do something with the response
    alert(response.statusText);
}

// Take a picture when cameraTrigger is tapped
cameraTrigger.onclick = function() {
    cameraSensor.width = cameraView.videoWidth;
    cameraSensor.height = cameraView.videoHeight;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
    cameraOutput.src = cameraSensor.toDataURL("image/webp");
    cameraOutput.classList.add("taken");
    
    postData(cameraOutput.src);
};

// Start the video stream when the window loads
window.addEventListener("load", cameraStart, false);