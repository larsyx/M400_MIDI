from fastapi.exception_handlers import http_exception_handler
from Database.database import DBSession
from fastapi import FastAPI, Request
from app.api import admin_routes, ws_routes, login_routes, user_routes, mixer_routes, video_routes
from fastapi.staticfiles import StaticFiles
import os
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException


templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "view", "static"))

app = FastAPI()

app.include_router(admin_routes.router)
app.include_router(login_routes.router)
app.include_router(ws_routes.router)
app.include_router(user_routes.router)
app.include_router(mixer_routes.router)
app.include_router(video_routes.router)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "view", "static")), name="static")


@app.on_event("shutdown")
def shutdown_event():
    DBSession.close()


#exception handler
# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
#     if exc.status_code == 401:
#         return templates.TemplateResponse("unauthorized.html", {"request": request})
#     if exc.status_code == 404:
#         return templates.TemplateResponse("notfound.html", {"request": request})
#     return await http_exception_handler(request, exc)