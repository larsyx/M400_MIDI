function openNav() {
    document.getElementById("profile-nav").style.width = "250px";
}

function closeNav() {
    document.getElementById("profile-nav").style.width = "0";
}


function openSaveNav(){
    document.getElementById("profile-save-nav").style.width = "250px";
}

function closeSaveNav() {
    document.getElementById("profile-save-nav").style.width = "0";
}

function saveProfile(id){
    const rawProfiles = getProfileChannelsValue();

    const profiles = Object.entries(rawProfiles).map(([key, value]) => ({
        channel: key,
        value: value
    }));

    const profile = {
        id : id,
        profiles: profiles
    };

    const xhttp = new XMLHttpRequest();
    xhttp.open("PUT", "./updateProfile");
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");


    xhttp.onreadystatechange = () => {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            const status = xhttp.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                location.reload();
            } else {
                alert("errore");
            }
        }
    }

    xhttp.send(JSON.stringify(profile));
        
}

function saveNewProfile(){
    el = document.getElementById("name-profile");

    if(el){
        if(el.value==null || el.value=="")
            alert("nome non inserito");
        else{
            const rawProfiles = getProfileChannelsValue();

            const profiles = Object.entries(rawProfiles).map(([key, value]) => ({
                channel: key,
                value: value
            }));

            const profile = {
                name: el.value,
                profiles: profiles
            };

            const xhttp = new XMLHttpRequest();
            xhttp.open("POST", "./createProfile");
            xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

            xhttp.onreadystatechange = () => {
                if (xhttp.readyState === XMLHttpRequest.DONE) {
                    const status = xhttp.status;
                    if (status === 0 || (status >= 200 && status < 400)) {
                        location.reload();
                    } else {
                        alert("errore");
                    }
                }
            }

            xhttp.send(JSON.stringify(profile));
        }
    }
}

function loadProfile(id, name){
    const xhttp = new XMLHttpRequest();

    const params = new URLSearchParams({
        profile_id: id
    });

    xhttp.open("GET", `./getProfile?${params.toString()}`);

    xhttp.onreadystatechange = () => {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            const status = xhttp.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                
                const response = JSON.parse(xhttp.responseText);
                const responseJson = JSON.parse(response);

                if(responseJson!=null){
                    for(const key in responseJson){
                        let element = document.getElementById("canale_" + key);
                        if(element !=null)
                            element.value = parseInt(responseJson[key], 10);
                    }

                    closeNav();
                    document.getElementsByClassName("profile-name")[0].innerHTML = name;


                    // style
                    const profiles = document.getElementsByClassName("profile-item"); 

                    Array.from(profiles).forEach(p => {
                        p.classList.remove("selected");
                    });

                    profile = document.getElementById(`profile_${id}`);
                    if(profile){
                        profile.classList.add("selected");
                    }
                }
            } else {
                alert("errore");
            }
        }
    }

    xhttp.send();
}

function getProfileChannelsValue(){
    let profile = {};

    let inputs = document.getElementsByClassName("inputRange");

    Array.from(inputs).forEach(element => {
        const match = element.id.match(/\d+$/);
        const numero = match ? match[0] : null;

        if (numero !== null) {
            profile[numero] = element.value;
        }
    });

    return profile;
}

function deleteProfiles(){
    if(confirm('Sei sicuro di voler eliminare tutti i profili?')){
        const xhttp = new XMLHttpRequest();

        xhttp.open("DELETE", `./deleteProfiles`);

        xhttp.onreadystatechange = () => {
            if (xhttp.readyState === XMLHttpRequest.DONE) {
                const status = xhttp.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                    location.reload();
                } else {
                    alert("errore");
                }
            }
        }

        xhttp.send();
    }
}

function deleteProfile(id){
    if(confirm('Sei sicuro di voler eliminare il profilo?')){
        const xhttp = new XMLHttpRequest();

        const params = new URLSearchParams({
            profile_id: id
        });
        xhttp.open("DELETE", `./deleteProfile?${params.toString()}`);

        xhttp.onreadystatechange = () => {
            if (xhttp.readyState === XMLHttpRequest.DONE) {
                const status = xhttp.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                    location.reload();
                } else {
                    alert("errore");
                }
            }
        }
        xhttp.send();
    }
}