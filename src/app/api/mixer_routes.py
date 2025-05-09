from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.auth.security import get_current_user, verify_mixer
from app.services.mixer_controller import MixerController

router = APIRouter()
mixerController = MixerController()

@router.get("/mixer/home", response_class=HTMLResponse)
async def home(request : Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])   

    return mixerController.loadFader(request)


@router.post("/mixer/set")
async def setFader(request: Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])   
    
    data = await request.json()
    canaleId = data.get("canaleId")
    value = data.get("value")

    mixerController.setFaderValue(canaleId,value)

@router.post("/mixer/switch")
async def setSwitchChannel(request : Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])   

    data = await request.json()
    canaleId = data.get("canaleId")
    switch = data.get("switch")

    mixerController.setSwitchChannel(canaleId=canaleId, switch=switch)

