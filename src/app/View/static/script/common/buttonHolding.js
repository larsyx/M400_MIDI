function enableHoldClick(button) {
    let interval;
    let isTouch = false;

    const triggerClick = () => {
        if (typeof button.onclick === 'function') {
            button.onclick();
        } else {
            button.dispatchEvent(new Event('click'));
        }
    };

    const startClicking = () => {
        triggerClick(); 
        interval = setInterval(triggerClick, 100);
    };

    const stopClicking = () => {
        clearInterval(interval);
        interval = null;
    };

    button.addEventListener('touchstart', e => {
        isTouch = true;
        e.preventDefault(); 
        if (!interval) startClicking();
    });

    button.addEventListener('touchend', stopClicking);
    button.addEventListener('touchcancel', stopClicking);

    button.addEventListener('mousedown', e => {
        if (isTouch) return; 
        if (!interval) startClicking();
    });

    button.addEventListener('mouseup', stopClicking);
    button.addEventListener('mouseleave', stopClicking);

    button.addEventListener('click', () => {
        if (!interval) triggerClick();
    });
}

const sliders = document.getElementsByClassName('canale-container'); 

for (const slider of sliders) {
    const btns = slider.querySelectorAll('button[onclick]');
    btns.forEach(enableHoldClick);
}

const aux_containers = document.getElementsByClassName('aux-channels-container'); 

for (const aux of aux_containers) {
    const btns = aux.querySelectorAll('button[onclick]');
    btns.forEach(enableHoldClick);
}

const main = document.getElementsByClassName('main-fader')[0]; 
if(main){
    let btns = main.querySelectorAll('button[onclick]');
    btns.forEach(enableHoldClick);
}
const drumButton = document.getElementsByClassName('drum')[0];
if(drumButton){
    btns = drumButton.querySelectorAll('button[onclick]');
    btns.forEach(enableHoldClick);
}

const gain = document.getElementById('gain-container');
if(gain){
    btns = gain.querySelectorAll('button[onclick]');
    btns.forEach(enableHoldClick);
}