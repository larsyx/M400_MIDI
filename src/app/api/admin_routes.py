from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from app.auth.security import get_current_user, verify_admin
from app.services.admin_controller import AdminController
from app.services.scene_controller import SceneController 
router = APIRouter()


sceneController = SceneController()

import os

adminController = AdminController()

@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    user = get_current_user(request)
    verify_admin(user["sub"])

    index_path = os.path.join(os.path.dirname(__file__), ".." ,"View", "administration", "home.html")  
    return FileResponse(index_path)

@router.get("/admin/manageUser", response_class=HTMLResponse)
async def manageUser(request: Request):
    user = get_current_user(request)
    verify_admin(user["sub"])

    return adminController.loadManageUser(request, user["sub"])

@router.get("/admin/manageScene", response_class=HTMLResponse)
async def manageScene(request: Request):
    user = get_current_user(request)
    verify_admin(user["sub"])

    return sceneController.manageScene(request, user["sub"])

@router.post("/admin/createScene")
async def create_scene(request : Request, nome: str = Form(...), descrizione:str = Form(...)):
    user = get_current_user(request)
    verify_admin(user["sub"])
    return sceneController.create_scene(request, user["sub"], nome, descrizione)


@router.post("/admin/deleteScene")
async def delete_scene(id: int = Form(...), current_user: dict = Depends(get_current_user)):
    return sceneController.delete_scene(current_user["sub"], id)


@router.post("/admin/updateScene")
async def create_scene(nome: str = Form(...), descrizione:str = Form(...), current_user: dict = Depends(get_current_user)):
    return sceneController.update_scene(current_user["sub"], nome, descrizione)


@router.get("/admin/scene_{scene_id}/")
async def get_scene(request : Request, scene_id: int):
    user = get_current_user(request)
    verify_admin(user["sub"])
    
    return sceneController.get_scene(request, user["sub"], scene_id)

#update scene

#manage user scene
@router.post("/admin/scene_{scene_id}/addPartecipazione", response_class=HTMLResponse)
async def add_partecipanti_scena(request : Request, scene_id : int, username : str = Form(...), aux : str = Form(...)):
    user = get_current_user(request)
    verify_admin(user["sub"])

    return sceneController.add_partecipante(request, user["sub"], scene_id, username, aux)

@router.post("/admin/scene_{scene_id}/removePartecipazione", response_class=HTMLResponse)
async def add_partecipanti_scena(request : Request, scene_id : int, username : str = Form(...), aux : int = Form(...)):
    user = get_current_user(request)
    verify_admin(user["sub"])

    return sceneController.remove_partecipante(request, user["sub"], scene_id, username, aux)


@router.post("/admin/scene_{scene_id}/deleteScene", response_class=HTMLResponse)
async def add_partecipanti_scena(request : Request, scene_id : int):
    user = get_current_user(request)
    verify_admin(user["sub"])

    return sceneController.delete_scene(request, user["sub"], scene_id)

#user management
@router.get("/admin/getUsers")
async def get_users(current_user: dict = Depends(get_current_user)):
    userController = AdminController()
    return userController.get_all_users(current_user["sub"])

@router.post("/admin/createUser")
async def create_user(request: Request, username: str = Form(...), nome: str = Form(...), ruolo: str = Form(...)):
    user = get_current_user(request)
    verify_admin(user["sub"])

    return adminController.create_user(request, user["sub"], username, nome, ruolo)


@router.post("/admin/deleteUser", response_class=HTMLResponse)
async def delete_user(request : Request, username: str = Form(...)):
    user = get_current_user(request)
    verify_admin(user["sub"])

    return adminController.delete_user(request, user["sub"], username)



@router.post("/admin/updateUser")
async def update_user(username: str, nome: str, ruolo: str, current_user: dict = Depends(get_current_user)):

    userController = AdminController()
    return userController.update_user(current_user["sub"], username, nome, ruolo)


