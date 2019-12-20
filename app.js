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

function postData(data) {

    var photo = document.querySelector('#file').files[0]
    data = new FormData();

    data.append('file', photo);

    fetch("http://127.0.0.1:5000/", { method: 'POST', body: data })
        .then(function(response) {
            response.text().then(function (text) {
                console.log(text);
              });
        })
        .catch(function(error) {            
            console.log(error);    
        });
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

window.addEventListener('load', function() {
    document.querySelector('input[type="file"]').addEventListener('change', function() {
        if (this.files && this.files[0]) {                        
            postData(this.files)
        }
    });
  });
  
  