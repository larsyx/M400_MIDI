function switchLayout() {
    const link = document.getElementById('layout-style');
    const currentHref = link.getAttribute('href');

    if (currentHref.includes('/static/style/mixer/horizontal-layout.css')) {
        link.setAttribute('href', '/static/style/mixer/vertical-layout.css');
    } else {
        link.setAttribute('href', '/static/style/mixer/horizontal-layout.css');
    }
}


function sendMessage(canaleId, value) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./set", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
            canaleId: canaleId,
            value: value
    };

    xhttp.send(JSON.stringify(message));
}

function sendMessageMain(value){
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./set/main", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
            value: value,
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

function checkSwitch(canaleId, switchValue){
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./switch", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
        canaleId: canaleId,
        switch: switchValue
    };

    xhttp.send(JSON.stringify(message));
}


function checkSwitchMain(switchValue){
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./switch/main", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
        switch: switchValue
    };

    xhttp.send(JSON.stringify(message));
}

const socket = new WebSocket(`wss://${window.location.host}/ws/liveSyncVideo`); 

socket.onopen = function(){};

socket.onmessage = function(event){
    const response = JSON.parse(event.data);
    if(response != null){
        let elname = "";

        let element = null;
        if(response.type === "switch"){
            element = document.getElementById(elname+"switch_"+response.channel);
            if(element != null){
                element.checked = response.value;
            }
        }else if(response.type === "fader"){
            element = document.getElementById(elname+"canale_"+response.channel);
            if(element != null)
                element.value = response.value;
        }

    }
};

socket.onerror = function(error){
    message = document.querySelector(".alert");
    message.hidden = false;
    message.getElementsByTagName("p")[0].innerHTML = "Errore sincronizzazione: " + error.message;
};

socket.onclose = function(e){
    message = document.querySelector(".alert");
    message.hidden = false;
    message.getElementsByTagName("p")[0].innerHTML = "Disconnesso, nessuna sincronizzazione con il mixer <a href='./home'>ricarica la pagina</a>";

};


const buttonContainer = document.getElementById("scene-button");
button = buttonContainer.querySelector("button[type='menu']");
button.addEventListener("click", function() {
    const sceneContainer = document.querySelector(".scene-container-list");
    sceneContainer.classList.toggle("visible");
});
