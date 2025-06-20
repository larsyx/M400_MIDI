
from fastapi import  HTTPException, Request, status, WebSocket
from app.DAO.user_dao import UserDAO
from app.auth.auth import verify_token  

userDAO = UserDAO()

# Funzione che estrae l'utente corrente a partire dal token
def get_current_user(request : Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token mancante nei cookie")

    payload = verify_token(token)  # Verifica il token
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token non valido")
    elif userDAO.getUserByUsername(payload["sub"]) == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token non valido")

    return payload

def get_current_user_token(access_token):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token mancante nei cookie")

    payload = verify_token(access_token)  # Verifica il token
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token non valido")
    elif userDAO.getUserByUsername(payload["sub"]) == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token non valido")

    return payload

def verify_admin(user):
    if not userDAO.isAdmin(user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="non sei autorizzato")
    return True

def verify_mixer(user):
    if not userDAO.isMixer(user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="non sei autorizzato")
    return True

def verify_video(user):
    if not userDAO.isVideo(user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="non sei autorizzato")
    return True