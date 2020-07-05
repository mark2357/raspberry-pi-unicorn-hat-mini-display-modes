function on_click_mode_switch(e, mode_index) {
    
    // sends post request to server to set mode of LED display
    let baseUrl = window.location.href;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", baseUrl + 'change-mode/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // handles the response from the server
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            // alert(xhr.responseText);
            
            // finds all previously active buttons
            let activeItems = document.getElementsByClassName('active-mode')

            // removes the active mode class from the buttons
            if(activeItems.length > 0) {
                [].forEach.call(activeItems, function (element) {
                    element.classList.remove('active-mode');
                });
            }

            // adds the new active mode to the buttons
            e.classList.add('active-mode');
        }
    }
    xhr.send(JSON.stringify({
        'mode': mode_index
    }));
}

function on_click_shutdown() {
    
    // sends post request to server to shutdown the server
    let baseUrl = window.location.href;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", baseUrl + 'shutdown/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // handles the response from the server
    // xhr.onreadystatechange = function() {
    //     if (xhr.readyState == XMLHttpRequest.DONE) {
            
    //     }
    // }
    xhr.send();
}