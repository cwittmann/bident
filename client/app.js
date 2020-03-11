var userLat;
var userLng;

const cameraView = document.querySelector("#camera--view"),
    cameraSensor = document.querySelector("#camera--sensor"),
    cameraTrigger = document.querySelector("#camera--trigger")

function cameraStart() {
    if (window.stream) {
        window.stream.getTracks().forEach(track => {
            track.stop();
        });
      }

      // Set constraints for the video stream
    var constraints = { video: { facingMode: "environment" }, audio: false };

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

function postData(formData) {   
    // Local: http://192.168.2.103:5000/
    // Local: http://127.0.0.1:5000/
    // Web Server: https://cwittmann.pythonanywhere.com/
    
    fetch("https://cwittmann.pythonanywhere.com/", { method: 'POST', body: formData })
        .then(function(response) {
            response.text().then(function (response) {
                console.log(response);
                showDetails(response);
            });
        })
        .catch(function(response) {
            console.log(response);
            alert(response);
        });
}

function showDetails(response){
    
    if(response == 'No match found.'){
        showNoMatchDialog();
        return;
    }
    
    var responseJSON = JSON.parse(response);       

    id = responseJSON.id;
    name = responseJSON.name;
    description = responseJSON.description;
    certainty = responseJSON.certainty;    
    
    detailDialog = document.querySelector("#detail-dialog");
    detailDialog.style.display = "block";    

    detailsImage = document.querySelector("#details-image");
    detailsImage.src = "http://cwittmann.pythonanywhere.com/image/" + id;

    if (name != undefined){
        detailsName = document.querySelector("#details-name");
        detailsName.style.display = "block";
        detailsName.append(name);        
    }

    if (parent != undefined){
        var parent;
        $.each(dataObjects, function(idx, dataObject) {
            if (dataObject["id"] == parent){
                parent = dataObject;            
            }
          }); 
        detailsParent = document.querySelector("#details-parent");
        detailsParent.style.display = "block";
        detailsParent.append(parent.name);        
    }

    if (description != undefined){
        detailsDescription = document.querySelector("#details-description");
        detailsDescription.style.display = "block";
        detailsDescription.append(description);     
    }

    if (certainty != undefined){
        detailsCertainty = document.querySelector("#details-certainty");
        detailsCertainty.style.display = "block";
        detailsCertainty.append(certainty + " %");     
    }    
}

function showNoMatchDialog(){

    detailsImage = document.querySelector("#details-image");
    detailsImage.src = "images/icons/notfound.svg";

    detailDialog = document.querySelector("#detail-dialog");
    detailDialog.style.display = "block"; 
    
    detailsName = document.querySelector("#details-name");
    detailsName.style.display = "block";
    detailsName.append("No matches found");   
    
    detailsDescription = document.querySelector("#details-error");
    detailsDescription.style.display = "block";
    detailsDescription.append("Please try again from another perspective or select another matching algorithm in the settings."); 
}

function closeDetails(){
    detailDialog = document.querySelector("#detail-dialog");
    detailDialog.style.display = "none";
    window.location.href = "index.html";
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

function setGeolocation(position) {
    userLat = position.coords.latitude;
    userLng = position.coords.longitude;    
}

function handleGeolocationError(error){
    console.log("Could not set geolocation: " + error.code + " " + error.message)
}

// Take a picture when cameraTrigger is tapped
cameraTrigger.onclick = function() {
    cameraSensor.width = cameraView.videoWidth;
    cameraSensor.height = cameraView.videoHeight;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);    
    dataURL = cameraSensor.toDataURL('image/jpeg', 1.0);
    var blob = dataURItoBlob(dataURL);
    var formData = new FormData(document.forms[0]);
    formData.append("photo", blob);         
    formData.append("userLat", userLat);
    formData.append("userLng", userLng);

    postData(formData);
};

window.onload = () => {
    'use strict';

    // Register Service Worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker
               .register('./service-worker.js');
    }

    // Get Geolocation
    navigator.geolocation.getCurrentPosition(setGeolocation, handleGeolocationError);
  }

// Start the video stream when the window loads
window.addEventListener("load", cameraStart, false);


  