from fastapi.responses import RedirectResponse
from Database.database import DBSession
from models import User
from app.dao.user_dao import UserDAO
from ..auth.auth import create_access_token

class AuthService:
    def __init__(self):
        self.db = DBSession.get()

    def login(self, username):

        username = username.strip()

        user = self.db.query(User).filter(User.username == username).first()

        if user:
            token = create_access_token({"sub": user.username})
            result = {'success': True}

            result = RedirectResponse(url="/home", status_code=302)

            result.set_cookie(key="access_token", value=f"{token}", samesite="None", secure=True)
            
            return result
        else:
            return "Credenziali non valide"

    def home(self, username):
        userDAO = UserDAO()
        if(userDAO.is_admin(username)):
            return RedirectResponse(url = "/admin", status_code=302)
        elif(userDAO.is_mixer(username)):
            return RedirectResponse(url="/mixer/home", status_code=302)
        elif(userDAO.is_video(username)):
            return RedirectResponse(url="/video/home", status_code=302)
        else:
            return RedirectResponse(url = "/user/getScenes", status_code=302)