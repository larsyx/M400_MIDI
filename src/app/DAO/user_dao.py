
from Database.database import DBSession
from Models.utente import RuoloUtente, Utente


class UserDAO:
    def __init__(self):
        self.db = DBSession.get()

    def getUserByUsername(self, username):
        try:
            user = self.db.query(Utente).filter(Utente.username == username).first()
            return user
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None
        
    def isAdmin(self, username):
        try:
            user = self.getUserByUsername(username)

            if user:
                return user.ruolo == RuoloUtente.amministratore
            else:
                return False
        except Exception as e:
            print(f"Error checking admin status: {e}")
            return False


    def createUser(self, username, nome, ruolo):
        try:
            new_user = Utente(username=username, nome=nome, ruolo=RuoloUtente[ruolo])
            self.db.add(new_user)
            self.db.commit()
            return new_user
        except Exception as e:
            print(f"Error creating user: {e}")
            return None


    def deleteUser(self, username):
        try:
            user = self.getUserByUsername(username)
            if user:
                self.db.delete(user)
                self.db.commit()
                return user
            else:
                return None
        except Exception as e:
            print(f"Error deleting user: {e}")
            return None


    def updateUser(self, username, nome, ruolo):
        try:
            user = self.getUserByUsername(username)
            if user:
                user.nome = nome
                user.ruolo = RuoloUtente[ruolo]
                self.db.commit()
                return user
            else:
                return None
        except Exception as e:
            print(f"Error updating user: {e}")
            return None
        
    def getAllUsers(self):
        try:
            users = self.db.query(Utente).all()
            return users
        except Exception as e:
            print(f"Error retrieving all users: {e}")
            return None