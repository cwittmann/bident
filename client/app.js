var userLat;
var userLng;

// Shows a detail dialog window.
function showDetails(response){   
    closeDetails();    

    var responseJSON = JSON.parse(response); 
    success = responseJSON.success;
    
    if(!success){
        showNoMatchDialog();
        return;
    }

    id = responseJSON.id;
    name = responseJSON.name;
    description = responseJSON.description;
    certainty = responseJSON.certainty;
    parentId = responseJSON.parentId;        
    parentName = responseJSON.parentName;    
    
    showElement("#detail-dialog");
    setImageSrc("#details-image", "https://cwittmann.pythonanywhere.com/image/" + id);

    if (name != undefined){
        showElementWithText("#details-name", name);                   
    }

    if (parentId && parentName){        
        showElementWithText("#details-parent", parentName);
        $("#details-parent-text").click(function() { getBuildingFromServer(parentId); });        
    }

    if (description != undefined){
        showElementWithText("#details-description", description);    
    }

    if (certainty != undefined){
        showElementWithText("#details-certainty", certainty);   
    }    

    showElement("#details-confirm");
}

// Shows a detail dialog window if no matches are found.
function showNoMatchDialog(){    
    setImageSrc("#details-image", "images/icons/notfound.svg");
    showElement("#detail-dialog");
    showElementWithText("#details-name", "Kein Objekt gefunden");    
    showElementWithText("#details-error", "Bitte versuche es noch einmal aus einer anderen Perspektive.");    
    showElement("#details-confirm");
}

// Close detail window and clear its values.
function closeDetails(){
    hideAndClearElement("#details-name");
    hideAndClearElement("#details-parent");
    hideAndClearElement("#details-description");
    hideAndClearElement("#details-certainty");
    hideAndClearElement("#details-error");
    hideAndClearElement("#detail-dialog");
}

// Sets the image src of an element.
function setImageSrc(selector, imagePath){
    $(selector).attr("src", imagePath);
}

// Displays an element.
function showElement(selector){
    $(selector).css("display", "block");  
}

// Displays an element and appends text to it.
function showElementWithText(selector, text){
    $(selector).css("display", "block");    
    $(selector + "-text").append(text);      
}

// Hides an element.
function hideElement(selector){
    $(selector).css("display", "none");    
}

// Hides an element and clears its text.
function hideAndClearElement(selector){
    $(selector).css("display", "none");
    $(selector + "-text").html("");      
}

// Set the global geolocation variables for the device's latitude and longitude.
function setGeolocation(position) {
    userLat = position.coords.latitude;
    userLng = position.coords.longitude;    
}

// Logs an error message if geolocation could not be accessed.
function handleGeolocationError(error){
    console.log("Could not set geolocation: " + error.code + " " + error.message)
}

// Registers ServiceWorker. Required for Progressive Web App functionality, e.g. offline caching.
function registerServiceWorker(){
    'use strict';
    
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker
               .register('./service-worker.js');
    }
}

// Initializes the camera and adds a listener so that the camera button takes a photo when clicked.
function intializeCamera(){    
    cameraStart();
    cameraTrigger.addEventListener("click", takePhoto);
}

window.onload = () => {
    registerServiceWorker();    
    intializeCamera();    
    navigator.geolocation.getCurrentPosition(setGeolocation, handleGeolocationError);    
  }    


  