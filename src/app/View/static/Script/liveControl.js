let socket = new WebSocket("wss://localhost:8080/ws/liveControl");

socket.onopen = function(event) {
    console.log("connessione aperta");
}

socket.onmessage = function(event){
    const data = JSON.parse(event.data);
    let doc = getDocumentById(data.canaleId);
    doc.value = data.value;
}

socket.onclose = function(event) {
    console.log("connessione chiusa");
}

function sendMessage(canaleId, value) {
    const message = {
        canaleId: canaleId,
        value: value
    };
    socket.send(JSON.stringify(message));
}