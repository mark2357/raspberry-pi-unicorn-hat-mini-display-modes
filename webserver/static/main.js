function on_click_mode_switch(e, mode_index) {
    
    // sends post request to server to set mode of LED display
    let baseUrl = window.location.href;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", baseUrl + 'change-mode/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // handles the response from the server
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            updateActiveButtons(e);
        }
    }
    xhr.send(JSON.stringify({
        'mode': mode_index
    }));
}

function on_click_custom_text_update() {
    on_click_custom_text(document.getElementById('set-custom-text-button'));
}

function on_input_value_change() {
    document.getElementById('update-custom-text-button').disabled = false;
}

function on_click_custom_text(e) {
    
    // sends post request to server to shutdown the server
    let baseUrl = window.location.href;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", baseUrl + 'custom-text/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // handles the response from the server
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            updateActiveButtons(e);
            document.getElementById('update-custom-text-button').disabled = true;
        }
    }

    // gets text from input box
    let customText = document.getElementById('custom-text-input').value;
    // gets color from input box
    let customColor = document.getElementById('custom-color-input').value;

    xhr.send(JSON.stringify({
        'custom-text': customText,
        'custom-color': customColor
    }));
}


function on_click_shutdown() {
    
    // sends post request to server to shutdown the server
    let baseUrl = window.location.href;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", baseUrl + 'shutdown/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.send();
}

function updateActiveButtons(e) {
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