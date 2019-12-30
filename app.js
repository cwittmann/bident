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

function postDataFromFile(data) {

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

function postDataFromCamera(formData) {   
        fetch("http://192.168.2.103:5000/", { method: 'POST', body: formData })
            .then(function(response) {
                response.text().then(function (text) {
                    console.log(text);
                });
            })
            .catch(function(error) {            
                console.log(error);    
            });	   
}

function dataURItoBlob(dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    var byteString;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(dataURI.split(',')[1]);
    else
        byteString = unescape(dataURI.split(',')[1]);

    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

    // write the bytes of the string to a typed array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }

    return new Blob([ia], {type:mimeString});
}

// Take a picture when cameraTrigger is tapped
cameraTrigger.onclick = function() {
    cameraSensor.width = cameraView.videoWidth;
    cameraSensor.height = cameraView.videoHeight;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
    cameraOutput.classList.add("taken");
    dataURL = cameraSensor.toDataURL('image/jpeg', 1.0);
    var blob = dataURItoBlob(dataURL);
    var fd = new FormData(document.forms[0]);
    fd.append("canvasImage", blob);    
    
    postDataFromCamera(fd);
};

// Start the video stream when the window loads
window.addEventListener("load", cameraStart, false);

window.addEventListener('load', function() {
    document.querySelector('input[type="file"]').addEventListener('change', function() {
        if (this.files && this.files[0]) {                        
            postDataFromFile(this.files)
        }
    });
  });
  
  