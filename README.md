# M400_MIDI
Remote MIDI controller for the **Roland M-400 V-Mixer**.

---

## 🛠️ Setup Instructions

### 1. Create and activate a virtual environment

From the project root:

```bash
# Create the virtual environment
python -m venv venv

on Windows: .\venv\Scripts\activate
on macOs/Linux: source venv/bin/activate
```

### 2. install dependencies:
```bash
    pip install -r requirements.txt
```
### 3. create .env file on src directory

    #Midi setting
    Manufacturer_ID = 0x41
    Device_ID = 
    Model_ID = 
    Command_ID_Data_Set = 0x12
    Command_ID_Data_Request = 0x11
    Main_Post_Fix_Fader = 0x00, 0x0E
    Main_Post_Fix_Switch = 0x00, 0x0C 
    Main_Pre_Fix = 0x06, 0x00

    #Ip setting
    WEBSOCKET_IP = ipServer

    #authentication setting
    AUTH_KEY = "your key"

### 4. Run the server
from src directory
```bash
    uvicorn app.main:app \
    --host 0.0.0.0 \
     --port 8000 \
     --app-dir . \
     --ssl-keyfile=PATH_TO_KEY.PEM \
     --ssl-certfile=PATH_TO_CERT.PEM
```