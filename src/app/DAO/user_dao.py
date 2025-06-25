from Database.database import DBSession
from models.utente import RuoloUtente, Utente
from sqlalchemy.orm import Session

class UserDAO:
    def __init__(self):
        self.db = DBSession.get()

    def get_user_by_username(self, username):
        try:
            user = self.db.query(Utente).filter(Utente.username == username).first()
            return user if user else None
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None
        
    def is_admin(self, username):
        try:
            user = self.get_user_by_username(username)

            if user:
                return user.ruolo == RuoloUtente.amministratore
            else:
                return False
        except Exception as e:
            print(f"Error checking admin status: {e}")
            return False

    def is_mixer(self, username):
        try:
            user = self.get_user_by_username(username)

            if user:
                return user.ruolo == RuoloUtente.mixerista
            else:
                return False
        except Exception as e:
            print(f"Error checking mixer status: {e}")
            return False

    def is_video(self, username):
        try:
            user = self.get_user_by_username(username)

            if user:
                return user.ruolo == RuoloUtente.video
            else:
                return False
        except Exception as e:
            print(f"Error checking mixer status: {e}")
            return False

    def create_user(self, username, nome, ruolo):
        try:
            new_user = Utente(username=username, nome=nome, ruolo=RuoloUtente[ruolo])
            self.db.add(new_user)
            self.db.commit()
            return new_user
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def delete_user(self, username):
        try:
            user = self.get_user_by_username(username)
            if user:
                self.db.delete(user)
                self.db.commit()
                return user
            else:
                return None
        except Exception as e:
            print(f"Error deleting user: {e}")
            return None

    def update_user(self, username, nome, ruolo):
        try:
            user = self.get_user_by_username(username)
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
        
    def get_all_users(self):
        try:
            users = self.db.query(Utente).all()
            return users
        except Exception as e:
            print(f"Error retrieving all users: {e}")
            return None
        
    def get_only_user(self):
        try:
            users = self.db.query(Utente).filter(Utente.ruolo == RuoloUtente.utente)
            return users
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return None