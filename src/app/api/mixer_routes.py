from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.auth.security import get_current_user, verify_mixer
from app.services.mixer_controller import MixerController

router = APIRouter()
mixerController = MixerController()

@router.get("/mixer/home", response_class=HTMLResponse)
async def home(request : Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])   

    return mixerController.loadFader(request)


@router.post("/mixer/set")
async def setFader(request: Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])   
    
    data = await request.json()
    canaleId = data.get("canaleId")
    value = data.get("value")

    mixerController.setFaderValue(canaleId,value)

@router.post("/mixer/switch")
async def setSwitchChannel(request : Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])   

    data = await request.json()
    canaleId = data.get("canaleId")
    switch = data.get("switch")

    mixerController.setSwitchChannel(canaleId=canaleId, switch=switch)


@router.post("/mixer/set/main")
async def setFaderMain(request: Request):
    user_data = get_current_user(request)

    data = await request.json()
    value = data.get("value")

    mixerController.setMainFaderValue(value)

@router.post("/mixer/switch/main")
async def setSwitchMain(request: Request):
    user_data = get_current_user(request)

    data = await request.json()
    switch = data.get("switch")

    mixerController.setMainSwitchChannel(switch)


@router.post("/mixer/set/dca")
async def setFaderDCA(request: Request):
    user_data = get_current_user(request)

    data = await request.json()
    dca = data.get("dca_id")
    value = data.get("value")

    mixerController.setDcaFaderValue(dca, value)

@router.post("/mixer/switch/dca")
async def setSwitchDCA(request: Request):
    user_data = get_current_user(request)

    data = await request.json()
    dca = data.get("dca_id")
    switch = data.get("switch")

    mixerController.setDcaSwitchChannel(dca,  switch)


@router.get("/mixer/loadScene/{scene_id}")
async def loadScene(request: Request, scene_id: int):
    user = get_current_user(request)
    verify_mixer(user["sub"])   

    return mixerController.loadScene(scene_id)

@router.post("/mixer/EQset")
async def eqSet(request: Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    data = await request.json()
    channel = data.get("channel")
    typeFreq = data.get("typeFreq")
    typeEq = data.get("typeEq")
    value = data.get("value")


    mixerController.eqSet(channel, typeFreq, typeEq, value)

@router.get("/mixer/EQget/{channel}")
async def eqGet(request: Request, channel : int):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    return mixerController.eqGet(channel)


@router.post("/mixer/EQSwitch")
async def eqSwitchSet(request: Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    data = await request.json()
    channel = data.get("channel")
    switch = data.get("switch")

    mixerController.eqSwitchSet(channel, switch)

@router.get("/mixer/EQSwitch/{channel}")
async def eqSwitchGet(request: Request, channel: int):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    return mixerController.eqSwitchGet(channel)

@router.post("/mixer/PreampSet")
async def eqPreampSet(request: Request):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    data = await request.json()
    channel = data.get("channel")
    value = data.get("value")

    mixerController.eqPreampSet(channel, int(value))

@router.get("/mixer/PreampGet/{channel}")
async def eqPreampGet(request: Request, channel : int):
    user = get_current_user(request)
    verify_mixer(user["sub"])

    return mixerController.eqPreampGet(channel)