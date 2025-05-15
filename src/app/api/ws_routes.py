from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.auth.security import get_current_user_token, verify_mixer
from midi.midiController import MidiController, MidiMixerSync
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


@router.websocket("/ws/liveSyncMixer")
async def websocket(websocket: WebSocket):

    cookies = websocket.cookies
    session_id = cookies.get("access_token")
    user_id = get_current_user_token(session_id)
    verify_mixer(user_id["sub"])

    await websocket.accept()

    is_active=True

    async def send_back(type, channel_address, value):
        try:
            if is_active:
                channelDAO = ChannelDAO()

                #controllare tipi
                channel = channelDAO.get_channel_by_address(channel_address)
                
                response = {
                    "type" : type,
                    "channel" : channel.id,
                    "value" : value
                }

                await websocket.send_json(response)
        except Exception as e:
            print(f"errore {e}")
            

    sync = MidiMixerSync(send_back=send_back)

    try:
        while True:
            await websocket.receive_json()
            
    except WebSocketDisconnect:
        print("Il client ha chiuso la connessione.")
        sync.port.close()
    finally:
        is_active = False  

