function sendMessage(canaleId, value) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./set", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
            canaleId: canaleId,
            value: value,
            aux: aux
    };

    xhttp.send(JSON.stringify(message));
}

function sendMessageMain(value){
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./set/main", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
            value: value,
            aux:auxMain
    };

    xhttp.send(JSON.stringify(message));
}

function changeValue(canaleId, action){
    inputRange = document.getElementById("canale_"+canaleId);
    let value = parseInt(inputRange.value, 10);

    if(action == "plus")
        value = Math.min(value + 1, 100);
    else if(action == "minus")
        value = Math.max(value -1, 0);
    inputRange.value = value;

    if(canaleId == "main")
        sendMessageMain(value);
    else
        sendMessage(canaleId, value);
}

function changeDrum(action){
    inputsRange = document.getElementsByClassName("batteria");

    for(const input of inputsRange){
        let value = parseInt(input.value, 10);
        if(action == "plus")
            value = Math.min(value + 2, 100);
        else if(action == "minus")
            value = Math.max(value -2, 0);
        input.value = value;


        id = input.id.split("_")
        canaleId = id[1]
        sendMessage(canaleId, value);
    }
} 

let socket;
let isConneting = false;
const spinner = document.getElementById("spinner-container");


function syncFader(){
    if(spinner)
        spinner.hidden = false;
    const params = new URLSearchParams({
        aux: aux,
        auxMain: auxMain
    });
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", `./getFadersValue?${params.toString()}`);
    xhttp.send();

    xhttp.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE) {
            if (this.status === 200) {
                try {
                    const response = JSON.parse(this.responseText);
                    const responseJson = typeof response === "string" ? JSON.parse(response) : response;
                    if (responseJson != null) {
                        for (const key in responseJson) {
                            let element = document.getElementById("canale_" + key);
                            if (element != null)
                                element.value = parseInt(responseJson[key], 10);
                        }
                    }
                } catch (e) {
                    console.error("Errore nel parsing JSON:", e);
                }
            } else {
                console.warn("Errore nella richiesta:", this.status, this.statusText);
            }

            if (spinner)
                spinner.hidden = true;
        }
    }
}

// WebSocket connection
function createAndConnectWebSocket(){
    if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING || isConnecting)) {
        return;
    }

    isConnecting = true;

    syncFader();

    socket = new WebSocket(`wss://${window.location.host}/ws/liveSync`);

    socket.onopen = function(){
        message = {
            "address":aux,
            "addressMain": auxMain
        }
        socket.send(JSON.stringify(message));

        message = document.querySelector(".alert");
        message.hidden = true;
    };

    socket.onmessage = function(event){
        const response = JSON.parse(event.data);
        if(response != null){
            let element = null;
            element = document.getElementById("canale_"+response.channel);
                if(element != null)
                    element.value = response.value;

        }
    };

    socket.onerror = function(error){
        isConnecting = false;
        message = document.querySelector(".alert");
        if(message){
            message.hidden = false;
            message.getElementsByTagName("p")[0].innerHTML = "Errore sincronizzazione: " + error.message;
        }
    };

    socket.onclose = function(e){
        isConnecting = false;
        message = document.querySelector(".alert");
        message.hidden = false;
        message.getElementsByTagName("p")[0].innerHTML = "Disconnesso, nessuna sincronizzazione con il mixer <a href='#' onclick='createAndConnectWebSocket();'>ricarica la pagina</a>";
    };
}

document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible") {
    createAndConnectWebSocket();
  }
});

window.addEventListener("focus", () => {
  createAndConnectWebSocket();
});

window.addEventListener("pageshow", (event) => {
    if (event.persisted || socket.readyState !== WebSocket.OPEN) {
        createAndConnectWebSocket();
    }
});

createAndConnectWebSocket();