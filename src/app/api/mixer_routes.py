from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from app.DAO.channel_dao import ChannelDAO
from app.auth.security import get_current_user
from app.services.auth_controller import AuthController
import os

from app.services.mixer_controller import MixerController

router = APIRouter()

@router.get("/mixer/home", response_class=HTMLResponse)
async def home(request : Request):
    mixerController = MixerController()
    return mixerController.loadFader(request)


@router.post("/mixer/set")
async def setFader(request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    mixerController = MixerController()

    data = await request.json()
    canaleId = data.get("canaleId")
    value = data.get("value")

    mixerController.setFaderValue(canaleId,value)

@router.post("/mixer/switch")
async def setSwitchChannel(request : Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    mixerController = MixerController()

    data = await request.json()
    canaleId = data.get("canaleId")
    switch = data.get("switch")

    mixerController.setSwitchChannel(canaleId=canaleId, switch=switch)

