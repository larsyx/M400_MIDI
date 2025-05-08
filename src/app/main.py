from Database.database import DBSession
from midi.midiController import MidiController
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from app.api import admin_routes, ws_routes, login_routes, user_routes, mixer_routes
from fastapi.staticfiles import StaticFiles
import os
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
midicontr = MidiController("pedal")




app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # oppure specifica ["http://localhost:8080"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.include_router(admin_routes.router)
app.include_router(login_routes.router)
app.include_router(ws_routes.router)
app.include_router(user_routes.router)
app.include_router(mixer_routes.router)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "View", "static")), name="static")


@app.on_event("shutdown")
def shutdown_event():
    DBSession.close()