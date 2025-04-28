from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from app.DAO.channel_dao import ChannelDAO
from app.auth.security import get_current_user
from app.services.scene_controller import SceneController
from app.services.user_controller import UserController
from midi.midiController import MidiController

router = APIRouter()

@router.get("/user/getScenes", response_class=HTMLResponse)
async def getScenes(request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_data = get_current_user(access_token)
    sceneController = SceneController()

    return sceneController.get_all_user_scene(user_data["sub"], request)

    
@router.get("/user/scene_{scene_id}", response_class=HTMLResponse)
async def loadScene(request: Request, scene_id: int):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_data = get_current_user(access_token)
    userController = UserController()
    return userController.load_scene(userID = user_data["sub"], scenaID = scene_id, request=request)

@router.post("/user/set")
async def setFader(request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    midiController = MidiController("pedal")
    channelDao = ChannelDAO()

    data = await request.json()
    canaleId = data.get("canaleId")
    value = data.get("value")
    indirizzoAux = data.get("aux")

    canaleAddress = channelDao.get_channel_address(canaleId)
    
    if(canaleAddress != None):
        addressAuxhex = [int(x,16) for x in indirizzoAux.split(",")]
        channelAddresshex = [int(x,16) for x in canaleAddress.split(",")]

        indirizzo = channelAddresshex + addressAuxhex
        
        midiController.send_command(indirizzo, MidiController.convertValue(int(value)))
    
    