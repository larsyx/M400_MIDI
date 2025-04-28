from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from app.auth.security import get_current_user
from app.services.auth_controller import AuthController
import os

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root():
    index_path = os.path.join(os.path.dirname(__file__), ".." ,"View", "static", "index.html")  
    return FileResponse(index_path)

@router.post("/login")
async def login(username: str = Form(...)):
        
    auth_service = AuthController()

    result = auth_service.login(username)

    return result 


@router.get("/home", response_class=RedirectResponse)
async def home(request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_data = get_current_user(access_token)
    authController = AuthController() 
    return authController.home(user_data["sub"])