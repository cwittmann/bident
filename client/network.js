
// Sends a HTTP POST request to the server and defines its callback functions.
function postData(formData) {   
    // Local: http://192.168.2.103:5000/
    // Local: http://127.0.0.1:5000/   
    
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

// Sends a HTTP GET request to the server requesting data on a building with a specific id.
function getBuildingFromServer(buildingId) {
    fetch("https://cwittmann.pythonanywhere.com/building/" + buildingId, { method: 'GET' })
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