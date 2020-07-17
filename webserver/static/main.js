/**
 * @description
 * handles when a mode button is clicked
 * @param {element} e 
 * @param {number} mode_index the new mode index
 */
function on_click_mode_switch(e, mode_index) {

    // sends post request to server to set mode of LED display
    let content = JSON.stringify({
        'mode': mode_index
    });

    let handleResponseFunc = (xhr) => {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            updateActiveButtons(e);
            set_custom_text_button_text_set_mode();
        }
    }
    send_post_request('change-mode/', content, handleResponseFunc);
}

/**
 * @description
 * handles when the color input or text input value changes
 */
function on_input_value_change() {
    
    // if the active mode is the custom text mode then the custom text buttons text is changed to update
    if(document.getElementById('set-custom-text-button').classList.contains('active-mode')) {
        set_custom_text_button_text_update()        
    }
}

/**
 * @description
 * handles when the custom text button is clicked
 * @param {element} e 
 */
function on_click_custom_text(e) {
   
    // gets text from input box
    let customText = document.getElementById('custom-text-input').value;
    // gets color from input box
    let customColor = document.getElementById('custom-color-input').value;

    let content = JSON.stringify({
        'custom-text': customText,
        'custom-color': customColor
    });

    let handleResponseFunc = (xhr) => {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            updateActiveButtons(e);
            set_custom_text_button_text_set_mode()
        }
    }
    send_post_request('custom-text/', content, handleResponseFunc);
}


/**
 * @description
 * handles when the shutdown button is clicked
 */
function on_click_shutdown() {
    
    // sends post request to server to shutdown the server
    // let baseUrl = window.location.href;
    // let xhr = new XMLHttpRequest();
    // xhr.open("POST", baseUrl + 'shutdown/', true);
    // xhr.setRequestHeader('Content-Type', 'application/json');

    // xhr.send();
    send_post_request('shutdown/', null);
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

/**
 * @description
 * changes the text of the custom text button to the update text 
 */
function set_custom_text_button_text_update() {
    document.getElementById('set-custom-text-button').innerHTML = 'Update Custom Text';
}

/**
 * @description
 * changes the text of the custom text button to the display text 
 */
function set_custom_text_button_text_set_mode() {
    document.getElementById('set-custom-text-button').innerHTML = 'Display Custom Text';
}


/**
 * @description
 * sends request to server
 */
function send_post_request(urlExtension, requestContent, returnHandleFunc=null) {
  
    // sends post request to server to shutdown the server
    let baseUrl = window.location.href;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", baseUrl + urlExtension, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // handles the response from the server
    if(returnHandleFunc !== null) {
        xhr.onreadystatechange = () => {
            returnHandleFunc(xhr);
        }
    }

    // sends the request
    xhr.send(requestContent);
}
