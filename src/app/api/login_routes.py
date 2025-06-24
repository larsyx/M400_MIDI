from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from app.auth.security import get_current_user
from app.services.auth_controller import AuthController
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "View")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/login")
async def login(request : Request, username: str = Form(...)):
        
    auth_service = AuthController()

    result = auth_service.login(username)

    if isinstance(result, str):
        return templates.TemplateResponse("index.html", {"request": request, "error": result})
        
    return result 


@router.get("/home", response_class=RedirectResponse)
async def home(request: Request):
    user_data = get_current_user(request)
    
    authController = AuthController() 
    return authController.home(user_data["sub"])