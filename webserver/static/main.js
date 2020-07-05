function on_click(e, mode_index) {
    
    // sends post request to server to set mode of LED display
    let xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href, true);
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