from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from app.auth.security import get_current_user
from app.services.auth_service import AuthService
from fastapi.templating import Jinja2Templates
from app.dao.user_dao import UserDAO
from app.auth.auth import verify_token  

import os

router = APIRouter()
userDAO = UserDAO()
auth_service = AuthService()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "view")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return templates.TemplateResponse("index.html", {"request": request})    

    payload = verify_token(token)
    if payload is None:
        return templates.TemplateResponse("index.html", {"request": request})   
    elif userDAO.get_user_by_username(payload["sub"]) == None:
       return templates.TemplateResponse("index.html", {"request": request})   

    return auth_service.home(payload["sub"])
    

@router.post("/login")
async def login(request : Request, username: str = Form(...)):

    result = auth_service.login(username)

    if isinstance(result, str):
        return templates.TemplateResponse("index.html", {"request": request, "error": result})
        
    return result 


@router.get("/home", response_class=RedirectResponse)
async def home(request: Request):
    user_data = get_current_user(request)
    
    return auth_service.home(user_data["sub"])


@router.get("/logout", response_class=RedirectResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="access_token")
    return response