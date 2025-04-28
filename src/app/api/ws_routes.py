from fastapi import APIRouter, WebSocket

from midi.midiController import MidiController
from app.DAO.channel_dao import ChannelDAO
router = APIRouter()

@router.websocket("/ws/liveControl")
async def websocket(websocket: WebSocket):
    channelDAO = ChannelDAO()
    midiController = MidiController("pedal")
    await websocket.accept()
    while True:
        data = await websocket.receive_json()

        canaleId = data.get("canaleId")
        value = data.get("value")
        indirizzoAux = data.get("aux")

        canaleAddress = channelDAO.get_channel_address(canaleId)

        if(canaleAddress != None):
            addressAuxhex = [int(x,16) for x in indirizzoAux.split(",")]
            channelAddresshex = [int(x,16) for x in canaleAddress.split(",")]

            indirizzo = channelAddresshex + addressAuxhex
            
            midiController.send_command(indirizzo, MidiController.convertValue(value))
        response = {
            "canaleId" : 1,
            "value" : 50
        }

        await websocket.send_json(response)
