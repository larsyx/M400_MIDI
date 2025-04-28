from fastapi.responses import HTMLResponse
from Models import Utente, RuoloUtente
from Database.database import DBSession
from app.DAO.user_dao import UserDAO


class AdminController:
    def __init__(self):
        self.userDAO = UserDAO()

    def create_user(self, adminUser, username, nome, ruolo):
        try:
            if self.userDAO.isAdmin(adminUser):
                new_user = self.userDAO.createUser(username=username, nome=nome, ruolo=ruolo)
                return new_user != None
            else:
                return HTMLResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        
    def delete_user(self, adminUser, username):
        try:
            if self.userDAO.isAdmin(adminUser):
                user = self.userDAO.deleteUser(username)

                return user != None
            else:
                return False
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        
    
    def update_user(self, adminUser, username, nome, ruolo):
        try:
            if self.userDAO.isAdmin(adminUser):
                user = self.userDAO.updateUser(username)
                return True
            else:
                return False
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def get_all_users(self, adminUser):
        try:
            if self.userDAO.isAdmin(adminUser):
                users = self.userDAO.getAllUsers()
                return users
            else:
                return HTMLResponse(status_code=403, content="Non hai i permessi per accedere a questa risorsa")
        except Exception as e:
            print(f"Error retrieving all users: {e}")
            return None