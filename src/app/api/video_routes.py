
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.DAO.channel_dao import ChannelDAO
from app.DAO.layout_canale_dao import LayoutCanaleDAO
from app.auth.security import get_current_user, verify_video
from app.services.scene_controller import SceneController
from app.services.video_controller import VideoController

router = APIRouter()

sceneController = SceneController()
videoController = VideoController()


@router.get("/video/home")
async def loadScene(request: Request):
    user_data = get_current_user(request)
    verify_video(user_data["sub"])

    return videoController.loadScene(request)

@router.post("/video/set")
async def setFader(request: Request):
    user_data = get_current_user(request)
    verify_video(user_data["sub"])

    data = await request.json()
    canaleId = data.get("canaleId")
    value = data.get("value")

    videoController.setFader(canaleId, value)
    

@router.post("/video/set/main")
async def setFaderMain(request: Request):
    user_data = get_current_user(request)
    verify_video(user_data["sub"])

    data = await request.json()
    value = data.get("value")
    
    videoController.setFaderMain(value)
   
@router.post("/video/switch/main")
async def setSwitchMain(request: Request):
    user_data = get_current_user(request)
    verify_video(user_data["sub"])

    data = await request.json()
    value = data.get("switch")
    
    print("Switching main video to:", value)
    videoController.setSwitchMain(value)

    