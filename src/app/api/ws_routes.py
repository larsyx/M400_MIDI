from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/ws/liveControl")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        
        response = {
            "canaleId" : 1,
            "value" : 50
        }

        await websocket.send_json(response)
