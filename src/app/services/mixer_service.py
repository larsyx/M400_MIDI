import json
import os
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dao.channel_dao import ChannelDAO
from app.dao.dca_dao import DCA_DAO
from app.dao.aux_dao import AuxDAO
from midi.midi_controller import MidiController, MidiListener, call_type, get_eq_address_value, get_eq_channel
from dotenv import load_dotenv
import json


class MixerService:
    def __init__(self):
        self.channelDAO = ChannelDAO()
        self.dcaDAO = DCA_DAO()
        self.auxDAO = AuxDAO()

        load_dotenv()
        self.postMainFader = [int(val,16) for val in os.getenv("Main_Post_Fix_Fader").split(",")]
        self.postSwitch = [int(val,16) for val in os.getenv("Main_Post_Fix_Switch").split(",")]
        self.preMain = [int(val,16) for val in os.getenv("Main_Pre_Fix").split(",")]
        self.postEqSwitch = [int(val,16) for val in os.getenv("EQ_Post_Switch").split(",")]
        self.postName = [int(val,16) for val in os.getenv("Fader_Post_Name").split(",")]
        self.postLink = [int(val,16) for val in os.getenv("Fader_Post_link").split(",")]
        self.pre_preamp = [int(val,16) for val in os.getenv("Preamp_Pre").split(",")]
        self.post_preamp = [int(val,16) for val in os.getenv("Preamp_Post").split(",")]
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "view", "mixer"))
        self.midiController = MidiController()

    def load_fader(self, request):
        canali = self.channelDAO.get_all_channels()
        dca = self.dcaDAO.get_dca()
                    
        # get value canali
        
        listenAddressFader = []
        listenAddressSwitch = []
        listenAddressName = []
        listenAddressLink = []

        # initialize the list of addresses for request and listen
        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")] 
            
            listenAddressFader.append(channelAddress + self.postMainFader)
            listenAddressSwitch.append(channelAddress + self.postSwitch)
            listenAddressName.append(channelAddress + self.postName)
            listenAddressLink.append(channelAddress + self.postLink)

        for dcaChannel in dca:
            dcaFader = [int(x,16) for x in dcaChannel.indirizzoMidiFader.split(",")] 
            dcaSwitch = [int(x,16) for x in dcaChannel.indirizzoMidiSwitch.split(",")]

            listenAddressFader.append(dcaFader)
            listenAddressSwitch.append(dcaSwitch)
            listenAddressName.append(dcaFader[0:2] + self.postName)

        listenAddressFader.append(self.preMain + self.postMainFader)
        listenAddressSwitch.append(self.preMain + self.postSwitch)

        # channel request and listen
        resultsValue = MidiListener.init_and_listen(listenAddressFader, call_type.CHANNEL)
        resultsValueSet = []
        
        # get channel value
        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")] 
            try:
                resultsValueSet.append(resultsValue[tuple(channelAddress + self.postMainFader)])
            except KeyError as k:
                print("errore chiave ", k)
                resultsValueSet.append(0)

        # get dca value
        resultDcaValueSet = []

        for dcaChannel in dca:
            dcaAddress = [int(x,16) for x in dcaChannel.indirizzoMidiFader.split(",")] 
            try:
                resultDcaValueSet.append(resultsValue[tuple(dcaAddress)])
            except KeyError as k:
                print("errore chiave ", k)
                resultDcaValueSet.append(0)

        # get main fader value
        try:
            valueMain = resultsValue[tuple(self.preMain + self.postMainFader)]
        except KeyError as e:
            print(f"error key {e}")
            valueMain = 0


        # Channel switch get value and listen
        resultsValueSwitch = MidiListener.init_and_listen(listenAddressSwitch, call_type.SWITCH)     
        resultsValueSetSwitch = []
        
        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")] 
            try:
                resultsValueSetSwitch.append(resultsValueSwitch[tuple(channelAddress + self.postSwitch)])
            except KeyError as k:
                print("errore chiave ", k)
                resultsValueSetSwitch.append(0)

        resultDcaValueSetSwitch = []

        for dcaChannel in dca:
            dcaAddress = [int(x,16) for x in dcaChannel.indirizzoMidiSwitch.split(",")] 
            try:
                resultDcaValueSetSwitch.append(resultsValueSwitch[tuple(dcaAddress)])
            except KeyError as k:
                print("errore chiave ", k)
                resultDcaValueSetSwitch.append(0)

        try:
            switchMain = resultsValueSwitch[tuple(self.preMain + self.postSwitch)]
        except KeyError as e:
            print(f"error key {e}")
            switchMain = False


        # get names channel
        resultsValueName = MidiListener.init_and_listen(listenAddressName, call_type.NAME)       
        resultsValueSetName = []
        resultDcaValueSetName = []
        
        # get channel name
        for canale in canali:
            channelAddress = [int(x,16) for x in canale.indirizzoMidi.split(",")] 
            try:
                resultsValueSetName.append(resultsValueName[tuple(channelAddress + self.postName)])
            except KeyError as k:
                print("errore chiave ", k)
                resultsValueSetName.append(0)

        # get dca name

        for dcaChannel in dca:
            dcaAddress = [int(x,16) for x in dcaChannel.indirizzoMidiFader.split(",")] 
            try:
                resultDcaValueSetName.append(resultsValueName[tuple(dcaAddress[0:2] + self.postName)])
            except KeyError as k:
                print("errore chiave ", k)
                resultDcaValueSetName.append(0)

        # get link channel
        resultsValueLink = MidiListener.init_and_listen(listenAddressLink, call_type.SWITCH)    
        resultsValueSetLink = []

        for address in listenAddressLink:
            try:
                resultsValueSetLink.append(not resultsValueLink[tuple(address)])
            except KeyError as k:
                print("errore chiave ", k)
                resultsValueSetLink.append(False)

        # only the second link
        skip = False
        for i in range(len(resultsValueSetLink)-1):
            if not skip:
                if resultsValueSetLink[i]:
                    if resultsValueSetLink[i+1]:
                        resultsValueSetLink[i] = False
                        skip = True
                    if not resultsValueSetLink[i+1]:
                        resultsValueSetLink[i] = False
                        resultsValueSetLink[i+1] = True
                        skip = True
            else:
                skip = False

        coppieCanali = list(zip(canali, resultsValueSet, resultsValueSetSwitch, resultsValueSetName, resultsValueSetLink))

        #DCA
        coppieDca = list(zip(dca, resultDcaValueSet, resultDcaValueSetSwitch, resultDcaValueSetName))


        # get scene for recall
        with open(os.path.join(os.path.dirname(__file__), "..", "..", "Database", "scenes.json"), "r") as file:
            scene = json.load(file)

        scenes = scene.get('scenes', [])

        # auxs name
        listenAddressAuxName = []
        auxs = self.auxDAO.get_all_aux()
        for aux in auxs:
            auxAddress = [int(x,16) for x in aux.indirizzoMidiMain.split(",")]
            listenAddressAuxName.append(auxAddress + self.postName)

        resultsValueAuxName = MidiListener.init_and_listen(listenAddressAuxName, call_type.NAME) 
        resultsValueAuxSetName = {}

        for aux in auxs:
            auxAddress = [int(x,16) for x in aux.indirizzoMidiMain.split(",")] 
            try:
                resultsValueAuxSetName[aux.id] = resultsValueAuxName[tuple(auxAddress + self.postName)]
            except KeyError as k:
                print("errore chiave ", k)
                resultsValueAuxSetName[aux.id] = ""

        return self.templates.TemplateResponse("scene.html", {"request": request, "canali": coppieCanali, "dcas": coppieDca, "valueMain" : valueMain, "switchMain" : switchMain, "scenes" : scenes, "auxs" : resultsValueAuxSetName})

    def get_aux_parameters(self, aux_id):
        aux = self.auxDAO.get_aux_by_id(aux_id)
        channels = self.channelDAO.get_all_channels()
        if aux and channels:
            address_aux = [int(x, 16) for x in aux.indirizzoMidi.split(",")]

            aux_addresses_fader = []
            for channel in channels:
                channel_address = [int(x, 16) for x in channel.indirizzoMidi.split(",")]
                aux_addresses_fader.append(channel_address + address_aux)

            results_value = MidiListener.init_and_listen(aux_addresses_fader, call_type.CHANNEL)
           
            results_value_set = {}
            
            # get channel value
            for channel in channels:
                channel_address = [int(x,16) for x in channel.indirizzoMidi.split(",")] 
                try:
                    results_value_set[channel.id] = results_value[tuple(channel_address + address_aux)]
                except KeyError as k:
                    print("errore chiave ", k)
                    results_value_set[channel.id] = 0

            return json.dumps(results_value_set, indent=3)

        return None

    def set_fader_value(self, canaleId, value):

        canaleAddress = self.channelDAO.get_channel_address(canaleId)
        
        if(canaleAddress != None):
            channelAddresshex = [int(x,16) for x in canaleAddress.split(",")]

            indirizzo = channelAddresshex + self.postMainFader
            
            self.midiController.send_command(indirizzo, MidiController.convert_fader_to_hex(int(value)))

    def set_switch_channel(self, canaleId, switch):
        canaleAddress = self.channelDAO.get_channel_address(canaleId)
        
        if(canaleAddress != None):
            channelAddresshex = [int(x,16) for x in canaleAddress.split(",")]

            indirizzo = channelAddresshex + self.postSwitch
            self.midiController.send_command(indirizzo, MidiController.convert_switch_to_hex(switch))

    def set_main_fader_value(self, value):

        indirizzo = self.preMain + self.postMainFader
        
        self.midiController.send_command(indirizzo, MidiController.convert_fader_to_hex(int(value)))

    def set_main_switch_channel(self, switch):
    
        indirizzo = self.preMain + self.postSwitch
        self.midiController.send_command(indirizzo, MidiController.convert_switch_to_hex(switch))

    def set_dca_fader_value(self, dca_id, value):
        dca = self.dcaDAO.get_dca_by_id(dca_id)

        if dca:
            address = [int(x, 16) for x in dca.indirizzoMidiFader.split(",")]
            self.midiController.send_command(address, MidiController.convert_fader_to_hex(int(value)))

    def set_dca_switch_channel(self, dca_id, switch):
        dca = self.dcaDAO.get_dca_by_id(dca_id)

        if dca:
            address = [int(x, 16) for x in dca.indirizzoMidiSwitch.split(",")]
            self.midiController.send_command(address, MidiController.convert_switch_to_hex(switch))

    def load_scene(self, scene_id):

        self.midiController.load_scene(scene_id)

        return RedirectResponse(url="/mixer/home", status_code=303)

    def eq_set(self, channel, typeFreq, typeEQ, value):
        if channel:
            channel_address = self.channelDAO.get_channel_address(channel)
            if channel_address:
                address, data = get_eq_address_value(typeFreq, typeEQ, float(value))

                channel_address = [int(x, 16) for x in channel_address.split(',')]
                address = channel_address + address

                self.midiController.send_command(address, data)
        return None

    def eq_get(self, channel):
        if channel:
            channel_address = self.channelDAO.get_channel_address(channel)

            if channel_address:
                channel_address = [int(x, 16) for x in channel_address.split(',')]

                channelsQ = get_eq_channel(channel_address, call_type.Q)
                channelsFreq = get_eq_channel(channel_address, call_type.FREQ)
                channelsGain = get_eq_channel(channel_address, call_type.GAIN)

                #get Q values
                resultsValueQ = MidiListener.init_and_listen(list(channelsQ.values()) , call_type.Q)

                for keychannel, channel in channelsQ.items():
                    for key, ch in resultsValueQ.items():
                        if tuple(channel) == key:
                            channelsQ[keychannel] = resultsValueQ[key]

                #get Freq values
                resultsValueFreq = MidiListener.init_and_listen(list(channelsFreq.values()) , call_type.FREQ)

                for keychannel, channel in channelsFreq.items():
                    for key, ch in resultsValueFreq.items():
                        if tuple(channel) == key:
                            channelsFreq[keychannel] = resultsValueFreq[key]

                #get gain values
                resultsValueGain = MidiListener.init_and_listen(list(channelsGain.values()) , call_type.GAIN)

                for keychannel, channel in channelsGain.items():
                    for key, ch in resultsValueGain.items():
                        if tuple(channel) == key:
                            channelsGain[keychannel] = resultsValueGain[key]


                low = {}
                low_mid = {}
                mid_hi = {}
                high = {}

                low_mid["q"] = channelsQ["eq_low_mid_q"]
                mid_hi["q"] = channelsQ["eq_mid_hi_q"]

                low["freq"] = channelsFreq["eq_low_freq"]
                low_mid["freq"] = channelsFreq["eq_low_mid_freq"]
                mid_hi["freq"] = channelsFreq["eq_mid_hi_freq"]
                high["freq"] = channelsFreq["eq_high_freq"]

                low["gain"] = channelsGain["eq_low_gain"]
                low_mid["gain"] = channelsGain["eq_low_mid_gain"]
                mid_hi["gain"] = channelsGain["eq_mid_hi_gain"]
                high["gain"] = channelsGain["eq_high_gain"]

                combined = [low, low_mid, mid_hi, high]

                return json.dumps(combined, indent=3)

        return None

    def eq_switch_set(self, channel, switch):
        if channel:
            channel_address = self.channelDAO.get_channel_address(channel)
            if channel_address:
                
                channel_address = [int(x, 16) for x in channel_address.split(',')]
                address = channel_address + self.postEqSwitch

                data = MidiController.convert_switch_to_hex(not switch)

                self.midiController.send_command(address, data)
        return None
    
    def eq_switch_get(self, channel):
        if channel:
            channel_address = self.channelDAO.get_channel_address(channel)
            if channel_address:
                
                channel_address = [int(x, 16) for x in channel_address.split(',')]
                address = channel_address + self.postEqSwitch
                
                # channel request and listen
                resultsValue = MidiListener.init_and_listen([address], call_type.SWITCH)

                value = next(iter(resultsValue.values()))
                return not value

    def eq_preamp_set(self, channel, value):
        if channel and 0 <= value <= 55:
            channel_address = self.pre_preamp + [channel] + self.post_preamp
            self.midiController.send_command(channel_address, [value])

    def eq_preamp_get(self, channel):
        if channel:
            
            channel_address = self.channelDAO.get_channel_address(channel)

            if channel_address:

                channel_address = [int(x, 16) for x in channel_address.split(',')]
                channel_address[0] -= 1
                channel_address += self.postName

                resultsValue = MidiListener.init_and_listen([channel_address], call_type.PATCH_CHANNEL)

                value_patchbay = next(iter(resultsValue.values()))
                if 0 < value_patchbay < 80:
                    address_request = self.pre_preamp + [value_patchbay] + self.post_preamp
                    
                    # channel request and listen
                    resultsValue = MidiListener.init_and_listen([address_request], call_type.PREAMP)

                    value = next(iter(resultsValue.values()))
                else:
                    value_patchbay = -1
                    value = 0

                response = {
                    "ch_patch" : value_patchbay,
                    "preamp" : value
                }
                
                return json.dumps(response, indent=2)

    def set_fader_aux_value(self, auxId, canaleId, value):
        aux = self.auxDAO.get_aux_by_id(auxId)
        if aux:
            address_aux = [int(x,16) for x in aux.indirizzoMidi.split(",")]
            canaleAddress = self.channelDAO.get_channel_address(canaleId)
            if canaleAddress:
                channelAddresshex = [int(x,16) for x in canaleAddress.split(",")]

                indirizzo = channelAddresshex + address_aux

                self.midiController.send_command(indirizzo, MidiController.convert_fader_to_hex(int(value)))