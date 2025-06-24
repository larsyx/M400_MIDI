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
        console.log(canaleId)
        sendMessage(canaleId, value);
    }


} 

socket.onopen = function(){
    message = {
        "address":aux,
        "addressMain": auxMain
    }
    socket.send(JSON.stringify(message));
};

socket.onmessage = function(event){
    console.log(event.data);
    const response = JSON.parse(event.data);
    if(response != null){
        let element = null;
        element = document.getElementById("canale_"+response.channel);
            if(element != null)
                element.value = response.value;

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
    message.getElementsByTagName("p")[0].innerHTML = "Disconnesso, nessuna sincronizzazione con il mixer <a href='./'>ricarica la pagina</a>";
};