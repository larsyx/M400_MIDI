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

const inputRanges = document.querySelectorAll('input[type="range"]');

inputRanges.forEach(input => {
    input.addEventListener('mousedown', onCustomStart, { passive: false, capture: true });
    input.addEventListener('touchstart', onCustomStart, { passive: false, capture: true });
});

function isVertical(slider) {
    const rect = slider.getBoundingClientRect();
    return rect.height > rect.width;
}

function isClickOnThumb(e) {
    const slider = e.currentTarget;
    const rect = slider.getBoundingClientRect();
    const sliderValue = parseFloat(slider.value);
    const min = parseFloat(slider.min || 0);
    const max = parseFloat(slider.max || 100);
    const valueRatio = (sliderValue - min) / (max - min);

    const thumbSize = 30;

    if (isVertical(slider)) {
        const y = e.clientY || (e.touches && e.touches[0].clientY);
        const thumbY = rect.bottom - rect.height * valueRatio;
        return Math.abs(y - thumbY) < thumbSize;
    } else {
        const x = e.clientX || (e.touches && e.touches[0].clientX);
        const thumbX = rect.left + rect.width * valueRatio;
        return Math.abs(x - thumbX) < thumbSize;
    }
}


let isDragging = false;
let startCoord = 0;
let startValue = 0;
let activeSlider = null;

function onCustomStart(e) {
    if (!isClickOnThumb(e)) {
        e.preventDefault();
        e.stopPropagation();
    }

    const slider = e.currentTarget;
    activeSlider = slider;
    isDragging = true;
    startValue = parseFloat(slider.value);
    const vertical = isVertical(slider);

    startCoord = vertical
        ? (e.clientY || (e.touches && e.touches[0].clientY))
        : (e.clientX || (e.touches && e.touches[0].clientX));

    const moveHandler = (ev) => onCustomMove(ev, slider, startCoord, startValue, vertical);
    const endHandler = stopCustomDrag;

    document.addEventListener('mousemove', moveHandler);
    document.addEventListener('mouseup', endHandler);
    document.addEventListener('touchmove', moveHandler, { passive: false });
    document.addEventListener('touchend', endHandler);

    slider._moveHandler = moveHandler;
    slider._endHandler = endHandler;
}

function onCustomMove(e, slider, startCoord, startValue, vertical) {
    if (!isDragging) return;

    e.preventDefault(); 

    const currentCoord = vertical
        ? (e.clientY || (e.touches && e.touches[0].clientY))
        : (e.clientX || (e.touches && e.touches[0].clientX));

    const delta = currentCoord - startCoord;
    const sliderSize = vertical ? slider.offsetHeight : slider.offsetWidth;

    const percent = vertical ? -delta / sliderSize : delta / sliderSize;
    const range = parseFloat(slider.max) - parseFloat(slider.min);
    const step = parseFloat(slider.step) || 1;

    let newValue = startValue + percent * range;
    newValue = Math.round(newValue / step) * step;
    newValue = Math.max(slider.min, Math.min(slider.max, newValue));

    slider.value = newValue;
    slider.dispatchEvent(new Event('input'));
}

function stopCustomDrag() {
    isDragging = false;

    if (activeSlider) {
        document.removeEventListener('mousemove', activeSlider._moveHandler);
        document.removeEventListener('mouseup', activeSlider._endHandler);
        document.removeEventListener('touchmove', activeSlider._moveHandler);
        document.removeEventListener('touchend', activeSlider._endHandler);

        delete activeSlider._moveHandler;
        delete activeSlider._endHandler;
        activeSlider = null;
    }
}
