
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.DAO.channel_dao import ChannelDAO
from app.DAO.layout_canale_dao import LayoutCanaleDAO
from app.auth.security import get_current_user
from app.services.scene_controller import SceneController
from app.services.user_controller import UserController

router = APIRouter()

sceneController = SceneController()
userController = UserController()

@router.get("/user/getScenes", response_class=HTMLResponse)
async def getScenes(request: Request):
    user_data = get_current_user(request)

    return sceneController.get_all_user_scene(user_data["sub"], request)

    
@router.get("/user/scene_{scene_id}/", response_class=HTMLResponse)
async def loadScene(request: Request, scene_id: int):
    user_data = get_current_user(request)
    
    return userController.load_scene(userID = user_data["sub"], scenaID = scene_id, request=request)


@router.get("/user/scene_{scene_id}/layout", response_class=HTMLResponse)
async def setLayout(request: Request, scene_id: int):
    user_data = get_current_user(request)

    return userController.set_layout(userID = user_data["sub"], scenaID = scene_id, request=request)



@router.post("/user/scene_{scene_id}/set")
async def setFader(request: Request):
    user_data = get_current_user(request)

    data = await request.json()
    canaleId = data.get("canaleId")
    value = data.get("value")
    indirizzoAux = data.get("aux")

    userController.setFader(canaleId, value, indirizzoAux)
    

@router.post("/user/scene_{scene_id}/set/main")
async def setFaderMain(request: Request):
    user_data = get_current_user(request)

    data = await request.json()
    value = data.get("value")
    indirizzoAux = data.get("aux")
    
    userController.setFaderMain(value, indirizzoAux)
   
@router.post("/user/scene_{scene_id}/layout/addChannelLayout")
async def aggiungiCanaleLayout(request: Request, scene_id: int):
    user_data = get_current_user(request)
    

    layoutDAO = LayoutCanaleDAO()
    data = await request.json()
    layoutDAO.addLayoutCanale(user_data["sub"], scene_id, data.get("canale_id"), data.get("descrizione"))

    return True


@router.post("/user/scene_{scene_id}/layout/removeChannelLayout")
async def removeCanaleLayout(request: Request, scene_id: int):
    user_data = get_current_user(request)


    layoutDAO = LayoutCanaleDAO()
    data = await request.json()
    canale_id = data.get("canale_id")

    layoutDAO.removeLayoutCanale(user_data["sub"], scene_id, canale_id)

    channelDAO = ChannelDAO()
    channel = channelDAO.get_channel_by_id(canale_id)
    return f"{channel.nome} : {channel.descrizione}"

    
@router.post("/user/scene_{scene_id}/layout/updateLayout")
async def setLayouts(request: Request, scene_id : int):
    user_data = get_current_user(request)
    
    layoutDAO = LayoutCanaleDAO()   
    data = await request.json()

    channelslayout = data.get("channelsLayout")

    for layout in channelslayout:
        layoutDAO.setLayoutCanale(user_data["sub"], scene_id, layout.get("canaleId"), layout.get("posizione"), layout.get("descrizione"), layout.get("isBatteria"))

    return "Layout salvato con successo"