function switchLayout() {
    const link = document.getElementById('layout-style');
    const currentHref = link.getAttribute('href');

    if (currentHref.includes('/static/style/mixer/horizontal-layout.css')) {
        link.setAttribute('href', '/static/style/mixer/vertical-layout.css');
    } else {
        link.setAttribute('href', '/static/style/mixer/horizontal-layout.css');
    }
}

function sendMessageDca(dca_id, value) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./set/dca", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
        dca_id: dca_id,
        value: value
    };

    xhttp.send(JSON.stringify(message));
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

function sendMessageMain(value) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./set/main", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
        value: value,
    };

    xhttp.send(JSON.stringify(message));
}

function changeValue(canaleId, action, type) {
    let targetSlider;
    if (type == "dca"){
        inputRange = document.getElementById("dca_canale_" + canaleId);
        targetSlider = slidersMap.get("dca_" + canaleId);
    } else {
        inputRange = document.getElementById("canale_" + canaleId);
        targetSlider = slidersMap.get("canale_" + canaleId);
    }
    let value = parseInt(inputRange.value, 10);

    value = parseInt(targetSlider.getValue(), 10);

    if (action == "plus")
        value = Math.min(value + step, 100);
    else if (action == "minus")
        value = Math.max(value - step, 0);
    inputRange.value = value;

    if (type == "dca"){
        sendMessageDca(canaleId, value);
    }else if (canaleId == "main"){
        sendMessageMain(value);
    }else{
        sendMessage(canaleId, value);
    }

    targetSlider.setValue(value);

}

function checkSwitch(canaleId, switchValue) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./switch", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
        canaleId: canaleId,
        switch: switchValue
    };

    xhttp.send(JSON.stringify(message));
}


function checkSwitchDca(dca_id, switchValue) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./switch/dca", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
        dca_id: dca_id,
        switch: switchValue
    };

    xhttp.send(JSON.stringify(message));
}

function checkSwitchMain(switchValue) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./switch/main", true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
        switch: switchValue
    };

    xhttp.send(JSON.stringify(message));
}

let socket;
const spinner = document.getElementById("spinner-container");
let flag_start = false;

function createAndConnectWebSocket() {

    if (socket && socket.readyState === WebSocket.OPEN) {
        return;
    }

    if (socket && socket.readyState === WebSocket.CONNECTING) {
        socket.close();
    }

    isConnecting = true;

    if (flag_start) {
        if (spinner)
            spinner.hidden = false;
        syncFader();
        syncDca();
        syncAux();
    }
    else
        flag_start = true;

    socket = new WebSocket(`wss://${window.location.host}/ws/liveSyncMixer`);


    socket.onopen = function () {
        if (spinner)
            spinner.hidden = true;
        message = document.querySelector(".alert");
        message.hidden = true;
    };

    socket.onmessage = function (event) {
        const response = JSON.parse(event.data);
        if (response != null) {
            let elname = "";
            if (response.dca)
                elname = "dca_";

            let element = null;
            if (response.type === "switch")
                element = document.getElementById(elname + "switch_" + response.channel);
            if (element != null)
                element.checked = response.value;
            else if (response.type === "fader")
                element = document.getElementById(elname + "canale_" + response.channel);
            if (element != null)
                element.value = response.value;

        }
    };

    socket.onerror = function (error) {
        isConnecting = false;
        message = document.querySelector(".alert");
        message.hidden = false;
        message.getElementsByTagName("p")[0].innerHTML = "Errore sincronizzazione: " + error.message;
    };

    socket.onclose = function (e) {
        isConnecting = false;
        message = document.querySelector(".alert");
        message.hidden = false;
        message.getElementsByTagName("p")[0].innerHTML = "Disconnesso, nessuna sincronizzazione con il mixer <a href='#' onclick='ensureWebSocket()'>ricarica la pagina</a>";

    };
}

function ensureWebSocket() {
    if (!socket || socket.readyState === WebSocket.CLOSED || socket.readyState === WebSocket.CLOSING) {
        createAndConnectWebSocket();
    }
}

document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") {
        ensureWebSocket();
    }
});

window.addEventListener("focus", ensureWebSocket);
window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
        ensureWebSocket();
    }
});

createAndConnectWebSocket();

setInterval(ensureWebSocket, 5000);


function openScene() {
    const sceneContainer = document.querySelector(".scene-container-list");
    sceneContainer.classList.toggle("visible");
}


// Disposition

function openDisposition() {
    const dispositionContainer = document.querySelector(".disposition-container");
    dispositionContainer.classList.toggle("visible");
}

const sortable = new Sortable(document.getElementById("sortable-element"), {
    animation: 150,
    handle: ".drag",
    dataIdAttr: "id"
});
const list = document.getElementById("sortable-element")

let draggedItem = null;


function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('li:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

function saveDisposition() {
    const ul = document.getElementById("sortable-element");
    const items = ul.querySelectorAll("li");

    const order = Array.from(items).map(item => item.id);

    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "./saveDisposition", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    const message = {
        disposition: order
    };

    xhttp.send(JSON.stringify(message));

    xhttp.onload = function () {
        if (xhttp.status === 200) {
            window.location.reload();
        } else {
            alert("Errore nel salvataggio della disposizione");
        }
    };
}

function resetOrder() {
    const ul = document.getElementById("sortable-element");
    const items = ul.querySelectorAll("li");

    const ids = Array.from(items).map(li => li.id);

    const sortedIds = ids.sort((a, b) => Number(a) - Number(b));

    sortable.sort(sortedIds, true);
}

// sync fader
function syncFader() {
    fetch('/mixer/syncFader', { method: 'GET' })
        .then(data => data.json())
        .then(response => {
            const json = JSON.parse(response);

            const container = document.getElementById("canali-container");
            container.innerHTML = '';
            json.canali.forEach(element => {
                if (element.link != true) {
                    const div = document.createElement("div");
                    div.classList.add("canale-container");
                    div.innerHTML = `
                    <input id="switch_${element.id}" onchange="checkSwitch(${element.id}, this.checked)" type="checkbox" ${element.switch ? 'checked' : ''} hidden>
                    <label for="switch_${element.id}" class="mute">${element.channelName}</label>
                    <button type="button" onclick="changeValue(${element.id}, 'plus')">+</button>
                    <input class="inputRange vertical" type="range" min="0" max="100" value="${element.value}" id="canale_${element.id}" onchange="sendMessage(${element.id}, this.value);" oninput="sendMessage(${element.id}, this.value);">
                    <button type="button" onclick="changeValue(${element.id}, 'minus')">-</button>
                    <button class="eq-button" type="button" onclick="openEq(${element.id}, '${element.name}')" style="font-size: 12px;">EQ</button>
                    <span class="descrizione">${element.name ? `<strong>${element.name}</strong>` : ''}</span>
                    `;
                    container.appendChild(div);
                }
            });

            // sync aux... 
            const auxContainer = document.getElementById("aux-channels-id");

            const auxs = auxContainer.querySelectorAll('.aux-channels-container:not(:first-child)');
            auxs.forEach(aux => {
                auxContainer.removeChild(aux);
            });

            json.canali.forEach(element => {
                if (element.link != true) {
                    const div = document.createElement("div");
                    div.classList.add("aux-channels-container");
                    div.innerHTML = `
                        <button type="button" onclick="changeValueAux(${element.id}, 'plus')">+</button>
                        <input class="inputRange vertical" type="range" min="0" max="100" value="${element.value}" id="aux_canale_${element.id}" onchange="sendMessageAux(${element.id}, this.value);" oninput="sendMessageAux(${element.id}, this.value);">
                        <button type="button" onclick="changeValueAux(${element.id}, 'minus')">-</button>
                        <span class="descrizione">${element.name ? `<strong>${element.name}</strong>` : ''}</span>
                        `;
                    auxContainer.appendChild(div);
                }
            });

            document.getElementById("canale_main").value = json.valueMain;
            document.getElementById("switch_main").checked = json.switchMain;
        });
}


// sync dca
function syncDca() {
    fetch('/mixer/syncDCA', { method: 'GET' })
        .then(data => data.json())
        .then(response => {
            const container = document.getElementById("dca-container");
            container.innerHTML = '';

            const json = JSON.parse(response);
            json.dcas.forEach(element => {
                const div = document.createElement("div");
                div.classList.add("canale-container");
                div.innerHTML = `
                <input id="dca_switch_${element.id}" onchange="checkSwitchDca(${element.id}, this.checked)" type="checkbox" ${element.switch ? 'checked' : ''} hidden>
                <label for="dca_switch_${element.id}" class="mute">${element.nameDca}</label>
                <button type="button" onclick="changeValue(${element.id}, 'plus', 'dca')">+</button>
                <input class="inputRange vertical" type="range" min="0" max="100" value="${element.value}" id="dca_canale_${element.id}" onchange="sendMessageDca(${element.id}, this.value);" oninput="sendMessageDca(${element.id}, this.value);">
                <button type="button" onclick="changeValue(${element.id}, 'minus', 'dca')">-</button>
                <span class="descrizione">${element.name ? `<strong>${element.name}</strong>` : ''}</span>
            `;
                container.appendChild(div);
            });
        });
}

// sync aux
function syncAux() {
    fetch('/mixer/syncAux', { method: 'GET' })
        .then(data => data.json())
        .then(response => {
            const container = document.getElementById("aux-list-id");
            container.innerHTML = '';
            const json = JSON.parse(response);
            
            json.auxs.forEach(element => {
                if (element.link != true) {
                    const div = document.createElement("div");
                    const radio = document.createElement("input");
                    radio.type = "radio";
                    radio.id = `aux_${element.id}`;
                    radio.name = "aux";
                    radio.onchange = function () { loadAuxParameters(element.id); };
                    if ( aux_id_selected === element.id ) radio.checked = true;
                    const label = document.createElement("label");
                    label.htmlFor = `aux_${element.id}`;
                    label.innerHTML = `${element.nameAux}<br>${element.name}`;
                    div.classList.add("aux-item");
                    div.appendChild(radio);
                    div.appendChild(label);
                    container.appendChild(div);
                }
            });

        });
}

