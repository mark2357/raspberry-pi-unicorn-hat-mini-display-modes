/**
 * @description
 * handles when a mode button is clicked
 * @param {element} e 
 * @param {string} modeId the string id of the new mode
 */
function onClickModeSwitch(e, modeId) {

    // sends post request to server to set mode of LED display
    let content = JSON.stringify({
        'mode': modeId
    });

    let handleResponseFunc = (xhr) => {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if(xhr.status == 200) {
            updateActiveButtons(e);
            setCustomTextButtonTextSetMode();
            }
            else {
                console.error(`HTTP request failed with ${xhr.response}`);
            }
        }        
    }
    sendPostRequest('change-mode/', content, handleResponseFunc);
}

/**
 * @description
 * handles when the color input or text input value changes
 */
function onInputValueChange() {
    // if the active mode is the custom text mode then the custom text buttons text is changed to update
    if(document.getElementById('set-custom-text-button').classList.contains('active-mode')) {
        setCustomTextButtonTextUpdate()        
    }
}

/**
 * @description
 * handles when the custom text button is clicked
 * @param {element} e 
 */
function onClickCustomText(e) {
   
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
            if(xhr.status == 200) {
            updateActiveButtons(e);
            setCustomTextButtonTextSetMode();
            }
            else {
                console.error(`HTTP request failed with ${xhr.response}`);
            }
        }   
    }
    sendPostRequest('custom-text/', content, handleResponseFunc);
}


/**
 * @description
 * handles when the shutdown button is clicked
 */
function onClickShutdown() {
    
    // sends post request to server to shutdown the server
    // let baseUrl = window.location.href;
    // let xhr = new XMLHttpRequest();
    // xhr.open("POST", baseUrl + 'shutdown/', true);
    // xhr.setRequestHeader('Content-Type', 'application/json');

    // xhr.send();
    sendPostRequest('shutdown/', null);
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
function setCustomTextButtonTextUpdate() {
    document.getElementById('set-custom-text-button').innerHTML = 'Update Custom Text';
}

/**
 * @description
 * changes the text of the custom text button to the display text 
 */
function setCustomTextButtonTextSetMode() {
    document.getElementById('set-custom-text-button').innerHTML = 'Display Custom Text';
}


/**
 * @description
 * sends request to server
 */
function sendPostRequest(urlExtension, requestContent, returnHandleFunc=null) {
  
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
