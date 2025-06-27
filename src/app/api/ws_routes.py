from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.dao.dca_dao import DCA_DAO
from app.auth.security import get_current_user_token, verify_mixer, verify_video
from midi.midi_controller import MidiMixerSync, MidiUserSync, MidiVideoSync
from app.dao.channel_dao import ChannelDAO
from app.dao.aux_dao import AuxDAO
import os
from dotenv import load_dotenv

router = APIRouter()

@router.websocket("/ws/liveSync")
async def live_user(websocket: WebSocket):
    cookies = websocket.cookies
    session_id = cookies.get("access_token")
    user_id = get_current_user_token(session_id)

    await websocket.accept()

    is_active=True

    async def send_back(channel_address, value):
        try:
            if is_active:
                channelDAO = ChannelDAO()

                if(channel_address == 'main'):
                    channel = channel_address
                else:
                    channel = channelDAO.get_channel_by_address(channel_address).id
                
                response = {
                    "channel" : channel,
                    "value" : value
                }

                await websocket.send_json(response)
        except Exception as e:
            print(f"errore sync {e}")


    sync = None

    try:
        while True:
            data = await websocket.receive_json()
            add = data.get("address")
            addMain = data.get("addressMain")
            address = [int(val,0) for val in add.split(",")]
            addressMain = [int(val,0) for val in addMain.split(",")]
            if address:
                sync = MidiUserSync(sendback=send_back, address=address, addressMain=addressMain)
                address = None
            
    except WebSocketDisconnect:
        print("Il client ha chiuso la connessione.")
    finally:
        if sync:
            sync.stop()
        is_active = False      



@router.websocket("/ws/liveSyncMixer")
async def live_mixer(websocket: WebSocket):

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
    finally:
        if sync:
            sync.stop()
        is_active = False  


@router.websocket("/ws/liveMixerSync/aux/{aux_id}")
async def live_aux_mixer(websocket: WebSocket, aux_id: int):
    cookies = websocket.cookies
    session_id = cookies.get("access_token")
    user_id = get_current_user_token(session_id)
    verify_mixer(user_id["sub"])

    await websocket.accept()

    is_active=True

    async def send_back(channel_address, value):
        try:
            if is_active:
                channelDAO = ChannelDAO()

                if(channel_address == 'main'):
                    channel = channel_address
                else:
                    channel = channelDAO.get_channel_by_address(channel_address).id
                
                response = {
                    "channel" : channel,
                    "value" : value
                }

                await websocket.send_json(response)
        except Exception as e:
            print(f"errore sync {e}")

    auxDAO = AuxDAO()
    aux = auxDAO.get_aux_by_id(aux_id)
    address = [int(val,0) for val in aux.indirizzoMidi.split(",")]
    addressMain = [int(val,0) for val in aux.indirizzoMidiMain.split(",")]
    sync = MidiUserSync(sendback=send_back, address=address, addressMain=addressMain)
                

    try:
        while True:
            data = await websocket.receive_json()
            
    except WebSocketDisconnect:
        print("Il client ha chiuso la connessione.")
    finally:
        if sync:
            sync.stop()
        is_active = False      



@router.websocket("/ws/liveSyncVideo")
async def live_video(websocket: WebSocket):

    cookies = websocket.cookies
    session_id = cookies.get("access_token")
    user_id = get_current_user_token(session_id)
    verify_video(user_id["sub"])

    await websocket.accept()

    is_active=True

    async def send_back(type, channel_address, value):
        try:
            if is_active:

                if channel_address == 'main':
                    channel = channel_address
                else:
                    channelDAO = ChannelDAO()
                    channel = channelDAO.get_channel_by_address(channel_address)
                    channel = channel.id
                
                if channel:
                    response = {
                        "type" : type,
                        "channel" : channel,
                        "value" : value
                    }

                    await websocket.send_json(response)
        except Exception as e:
                print(f"errore liveSyncMixer {e}")
            
    load_dotenv()
    auxdao = AuxDAO()
    auxId = os.getenv("VIDEO_AUX_ID")
    aux = auxdao.get_aux_by_id(int(auxId))

    if(aux):
        address = [int(val,0) for val in aux.indirizzoMidi.split(",")]
        addressMain = [int(val,0) for val in aux.indirizzoMidiMain.split(",")]

    sync = MidiVideoSync(sendback=send_back, address=address, addressMain=addressMain)

    try:
        while True:
            await websocket.receive_json()
            
    except WebSocketDisconnect:
        print("Il client ha chiuso la connessione.")
    finally:
        if sync:
            sync.stop()
        is_active = False  

