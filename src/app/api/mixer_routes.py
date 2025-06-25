from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.auth.security import get_current_user, verify_mixer
from app.services.mixer_service import MixerService

router = APIRouter()
mixer_service = MixerService()

@router.get("/mixer/home", response_class=HTMLResponse)
async def home(request : Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])   

    return mixer_service.loadFader(request)


@router.post("/mixer/set")
async def set_fader(request: Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])   
    
    data = await request.json()
    canaleId = data.get("canaleId")
    value = data.get("value")

    mixer_service.setFaderValue(canaleId,value)

@router.post("/mixer/switch")
async def set_switch_channel(request : Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])   

    data = await request.json()
    canaleId = data.get("canaleId")
    switch = data.get("switch")

    mixer_service.setSwitchChannel(canaleId=canaleId, switch=switch)


@router.post("/mixer/set/main")
async def set_fader_main(request: Request):
    user_data = get_current_user(request)

    data = await request.json()
    value = data.get("value")

    mixer_service.setMainFaderValue(value)

@router.post("/mixer/switch/main")
async def set_switch_main(request: Request):
    user_data = get_current_user(request)

    data = await request.json()
    switch = data.get("switch")

    mixer_service.setMainSwitchChannel(switch)


@router.post("/mixer/set/dca")
async def set_fader_DCA(request: Request):
    user_data = get_current_user(request)

    data = await request.json()
    dca = data.get("dca_id")
    value = data.get("value")

    mixer_service.setDcaFaderValue(dca, value)

@router.post("/mixer/switch/dca")
async def set_switch_DCA(request: Request):
    user_data = get_current_user(request)

    data = await request.json()
    dca = data.get("dca_id")
    switch = data.get("switch")

    mixer_service.setDcaSwitchChannel(dca,  switch)


@router.get("/mixer/loadScene/{scene_id}")
async def load_scene(request: Request, scene_id: int):
    user = get_current_user(request)
    verify_mixer(user["sub"])   

    return mixer_service.loadScene(scene_id)

@router.post("/mixer/EQset")
async def eq_set(request: Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    data = await request.json()
    channel = data.get("channel")
    typeFreq = data.get("typeFreq")
    typeEq = data.get("typeEq")
    value = data.get("value")


    mixer_service.eqSet(channel, typeFreq, typeEq, value)

@router.get("/mixer/EQget/{channel}")
async def eq_get(request: Request, channel : int):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    return mixer_service.eqGet(channel)


@router.post("/mixer/EQSwitch")
async def eq_switch_set(request: Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    data = await request.json()
    channel = data.get("channel")
    switch = data.get("switch")

    mixer_service.eqSwitchSet(channel, switch)

@router.get("/mixer/EQSwitch/{channel}")
async def eq_switch_get(request: Request, channel: int):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    return mixer_service.eqSwitchGet(channel)

@router.post("/mixer/PreampSet")
async def eq_preamp_set(request: Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    data = await request.json()
    channel = data.get("channel")
    value = data.get("value")

    mixer_service.eqPreampSet(channel, int(value))

@router.get("/mixer/PreampGet/{channel}")
async def eq_preamp_get(request: Request, channel : int):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    return mixer_service.eqPreampGet(channel)


# aux 
@router.get("/mixer/aux/get/{aux_id}")
async def eq_preamp_get(request: Request, aux_id : int):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    return mixer_service.getAuxParameters(aux_id)

@router.post("/mixer/aux/set")
async def set_fader(request: Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])   
    
    data = await request.json()
    auxId = data.get("auxId")
    canaleId = data.get("canaleId")
    value = data.get("value")

    mixer_service.setFaderAuxValue(auxId, canaleId, value)