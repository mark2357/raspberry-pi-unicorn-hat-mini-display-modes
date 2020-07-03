function on_click(mode_index) {
    
    // sends post request to server to set mode of LED display
    let xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            alert(xhr.responseText);
        }
    }
    xhr.send(JSON.stringify({
        'mode': mode_index
    }));
}