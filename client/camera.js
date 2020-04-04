const cameraView = document.querySelector("#camera-view"),
    cameraSensor = document.querySelector("#camera-sensor"),
    cameraTrigger = document.querySelector("#camera-trigger")


// Displays the input of the back camera in the cameraView element.
function cameraStart() {
    
    // Stop all video stream tracks, e.g. if other application are still using the camera.
    if (window.stream) {
        window.stream.getTracks().forEach(track => {
            track.stop();
        });
    }
    
    // Choose back camera of device and mute audio.
    var constraints = { video: { facingMode: "environment" }, audio: false };
    
    // Connects the cameraView element to the first track of the video stream so that it shows its input.
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function(stream) {
        track = stream.getTracks()[0];
        cameraView.srcObject = stream;
    })
    .catch(function(error) {
        console.error("Could not load media devices.", error);
    });
}

// Converts a data URI to a blob image. 
// Code taken from https://gist.github.com/poeticninja/0e4352bc80bc34fad6f7
function dataURItoBlob(dataURI) {    
    var byteString;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(dataURI.split(',')[1]);
    else
        byteString = unescape(dataURI.split(',')[1]);
    
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }

    return new Blob([ia], {type:mimeString});
}

// Captures image, adds it to form and submits form to server.
function takePhoto(){    
    var blob = createBlobFromVideo();
    var formData = createFormData(blob);
    postData(formData);
}

// Creates form data including a blob image and the current geolocation.
function createFormData(blob){
    var formData = new FormData(document.forms[0]);
    formData.append("photo", blob);          
    formData.append("userLat", userLat);
    formData.append("userLng", userLng);   
    
    return formData;
}

// Captures an image from the video element of the main page and converts it to a blob.
function createBlobFromVideo(){
    cameraSensor.width = 720;
    cameraSensor.height = 1280;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0, 720, 1280);    
    dataURL = cameraSensor.toDataURL('image/jpeg', 1.0);

    return dataURItoBlob(dataURL);
}