from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from app.auth.security import get_current_user
from app.services.scene_controller import SceneController
from app.services.user_controller import UserController

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