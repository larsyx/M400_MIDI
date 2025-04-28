
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.auth import verify_token  

# Impostazione dello schema di autenticazione
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Funzione che estrae l'utente corrente a partire dal token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)  # Verifica il token
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token non valido")
    return payload
