from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.DAO.dca_dao import DCA_DAO
from app.auth.security import get_current_user_token, verify_mixer
from midi.midiController import MidiMixerSync, MidiUserSync
from app.DAO.channel_dao import ChannelDAO
router = APIRouter()

@router.websocket("/ws/liveSync")
async def websocket(websocket: WebSocket):
    cookies = websocket.cookies
    session_id = cookies.get("access_token")
    user_id = get_current_user_token(session_id)

    await websocket.accept()

    is_active=True

    async def send_back(channel_address, value):
        # try:
        if is_active:
            channelDAO = ChannelDAO()

            channel = channelDAO.get_channel_by_address(channel_address)
            
            response = {
                "channel" : channel.id,
                "value" : value
            }

            await websocket.send_json(response)
        # except Exception as e:
        #     print(f"errore sync {e}")

    try:
        while True:
            id = await websocket.receive_text()
            address = [int(val,0) for val in id.split(",")]
            if address:
                sync = MidiUserSync(sendback=send_back, address=address)
                address = None
            
    except WebSocketDisconnect:
        print("Il client ha chiuso la connessione.")
        sync.stop()
    finally:
        is_active = False      


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
                dca = False
                if channel_address == 'main':
                    channel = channel_address
                elif channel_address.count(',') == 3:
                    dcaDAO = DCA_DAO()
                    if(type == "fader"):
                        channel = dcaDAO.get_dca_by_address(channel_address)
                    elif(type == "switch"):
                        channel = dcaDAO.get_dca_by_address_switch(channel_address)
                    
                    channel = channel.id
                    dca = True

                else:
                    channelDAO = ChannelDAO()
                    channel = channelDAO.get_channel_by_address(channel_address)
                    channel = channel.id
                
                if channel:
                    response = {
                        "dca" : dca,
                        "type" : type,
                        "channel" : channel,
                        "value" : value
                    }

                    await websocket.send_json(response)
        except Exception as e:
                print(f"errore liveSyncMixer {e}")
            

    sync = MidiMixerSync(send_back=send_back)

    try:
        while True:
            await websocket.receive_json()
            
    except WebSocketDisconnect:
        print("Il client ha chiuso la connessione.")
        sync.stop()
    finally:
        is_active = False  


