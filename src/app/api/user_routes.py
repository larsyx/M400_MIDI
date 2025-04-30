
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from app.DAO.channel_dao import ChannelDAO
from app.DAO.layout_canale_dao import LayoutCanaleDAO
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

    
@router.get("/user/scene_{scene_id}/", response_class=HTMLResponse)
async def loadScene(request: Request, scene_id: int):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_data = get_current_user(access_token)
    userController = UserController()
    return userController.load_scene(userID = user_data["sub"], scenaID = scene_id, request=request)


@router.get("/user/scene_{scene_id}/layout", response_class=HTMLResponse)
async def setLayout(request: Request, scene_id: int):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_data = get_current_user(access_token)
    userController = UserController()
    

    return userController.set_layout(userID = user_data["sub"], scenaID = scene_id, request=request)



@router.post("/user/scene_{scene_id}/set")
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
    

@router.post("/user/scene_{scene_id}/set/main")
async def setFaderMain(request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    midiController = MidiController("pedal")

    data = await request.json()
    value = data.get("value")
    indirizzoAux = data.get("aux")
    
    addressAuxhex = [int(x,16) for x in indirizzoAux.split(",")]

    midiController.send_command(addressAuxhex, MidiController.convertValue(int(value)))
   
@router.post("/user/scene_{scene_id}/layout/addChannelLayout")
async def aggiungiCanaleLayout(request: Request, scene_id: int, canale_id : int = Form(...), posizione: str = Form(...), descrizione: str = Form(...)):
    access_token = request.cookies.get("access_token")

    user_data = get_current_user(access_token)

    if not user_data:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    layoutDAO = LayoutCanaleDAO()

    layoutDAO.addLayoutCanale(user_data["sub"], scene_id, canale_id, posizione, descrizione)

    return RedirectResponse(url="./", status_code=302)


@router.post("/user/scene_{scene_id}/layout/removeChannelLayout")
async def removeCanaleLayout(request: Request, scene_id: int, canale_id : int = Form(...)):
    access_token = request.cookies.get("access_token")

    user_data = get_current_user(access_token)

    if not user_data:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

    layoutDAO = LayoutCanaleDAO()

    if layoutDAO.removeLayoutCanale(user_data["sub"], scene_id, canale_id):
        print(True)

    return RedirectResponse(url="./", status_code=302)

    
@router.post("/user/scene_{scene_id}/layout/updateLayout")
async def setLayouts(request: Request, scene_id : int):
    access_token = request.cookies.get("access_token")

    user_data = get_current_user(access_token)

    if not user_data:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    layoutDAO = LayoutCanaleDAO()   
    data = await request.json()

    channelslayout = data.get("channelsLayout")

    for layout in channelslayout:
        layoutDAO.setLayoutCanale(user_data["sub"], scene_id, layout.get("canaleId"), layout.get("posizione"), layout.get("descrizione"))

    return "Layout salvato con successo"