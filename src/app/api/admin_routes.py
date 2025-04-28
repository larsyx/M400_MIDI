from fastapi import APIRouter, Depends, Form
from app.auth.security import get_current_user
from fastapi.responses import HTMLResponse, FileResponse
from Models import RuoloUtente
from app.services.admin_controller import AdminController
from app.services.scene_controller import SceneController 
router = APIRouter()


@router.get("/admin")
async def admin():
    return ""

@router.post("/admin/createScene")
async def create_scene(nome: str = Form(...), descrizione:str = Form(...), current_user: dict = Depends(get_current_user)):
    sceneController = SceneController()
    return sceneController.create_scene(current_user["sub"], nome, descrizione)


@router.post("/admin/deleteScene")
async def delete_scene(id: int = Form(...), current_user: dict = Depends(get_current_user)):
    sceneController = SceneController()
    return sceneController.delete_scene(current_user["sub"], id)


@router.post("/admin/updateScene")
async def create_scene(nome: str = Form(...), descrizione:str = Form(...), current_user: dict = Depends(get_current_user)):
    sceneController = SceneController()
    return sceneController.update_scene(current_user["sub"], nome, descrizione)

@router.get("/admin/getScenes")
async def get_scenes(current_user: dict = Depends(get_current_user)):
    sceneController = SceneController()
    return sceneController.get_all_scene(current_user["sub"])

@router.post("/admin/getScene")
async def get_scene(id: int = Form(...), current_user: dict = Depends(get_current_user)):
    sceneController = SceneController()
    return sceneController.get_scene(current_user["sub"], id)

#update scene


#get aux, channel, user
@router.get("/admin/getAuxs")
async def get_aux(current_user: dict = Depends(get_current_user)):
    return ""

@router.get("/admin/getChannels")
async def get_channel(current_user: dict = Depends(get_current_user)):
    return ""



#user management
@router.get("/admin/getUsers")
async def get_users(current_user: dict = Depends(get_current_user)):
    userController = AdminController()
    return userController.get_all_users(current_user["sub"])

@router.post("/admin/createUser")
async def create_user(username: str = Form(...), nome: str = Form(...), ruolo: str = Form(...), current_user: dict = Depends(get_current_user)):
    userController = AdminController()
    return userController.create_user(current_user["sub"], username, nome, ruolo)


@router.post("/admin/deleteUser")
async def delete_user(username: str, current_user: dict = Depends(get_current_user)):
    userController = AdminController()
    return userController.delete_user(current_user["sub"], username)



@router.post("/admin/updateUser")
async def update_user(username: str, nome: str, ruolo: str, current_user: dict = Depends(get_current_user)):

    userController = AdminController()
    return userController.update_user(current_user["sub"], username, nome, ruolo)


