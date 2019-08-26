#!/usr/bin/env python3

import eel
import argparse
import os
import platform
import struct
import sys
from datetime import datetime
from threading import Thread
import numpy as np
import soundfile
from forex_python.bitcoin import BtcConverter
import multiprocessing
import json
from requests.exceptions import HTTPError
import pyaudio
import wave
import simpleaudio as sa
import speech_recognition as speech_rec
from xml.dom import minidom
import xml.etree.ElementTree as ET
import requests
from forex_python.converter import CurrencyRates
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from seleniumrequests import Chrome
from selenium.webdriver.chrome.options import Options
import socket
from kamene.all import *
from netaddr import IPNetwork
import geocoder
try:
    import snowboydecoder
except:
    print("Snowboy hotword detection is not supported on windows")
    sys.path.append(os.path.join(os.path.dirname(__file__), 'binding/python'))
    from porcupine import Porcupine

inconvo=False

browser=None

latlong=None

contextresettimers=[]

detector=None


class PorcupineDemo(Thread):

    """
    Demo class for wake word detection (aka Porcupine) library. It creates an input audio stream from a microphone,
    monitors it, and upon detecting the specified wake word(s) prints the detection time and index of wake word on
    console. It optionally saves the recorded audio into a file for further review.
    """

    def __init__(
            self,
            library_path,
            model_file_path,
            keyword_file_paths,
            sensitivities,
            input_device_index=None,
            output_path=None):

        """
        Constructor.

        :param library_path: Absolute path to Porcupine's dynamic library.
        :param model_file_path: Absolute path to the model parameter file.
        :param keyword_file_paths: List of absolute paths to keyword files.
        :param sensitivities: Sensitivity parameter for each wake word. For more information refer to
        'include/pv_porcupine.h'. It uses the
        same sensitivity value for all keywords.
        :param input_device_index: Optional argument. If provided, audio is recorded from this input device. Otherwise,
        the default audio input device is used.
        :param output_path: If provided recorded audio will be stored in this location at the end of the run.
        """

        super(PorcupineDemo, self).__init__()

        self._library_path = library_path
        self._model_file_path = model_file_path
        self._keyword_file_paths = keyword_file_paths
        self._sensitivities = sensitivities
        self._input_device_index = input_device_index

        self._output_path = output_path
        if self._output_path is not None:
            self._recorded_frames = []

    def run(self):
        """
         Creates an input audio stream, initializes wake word detection (Porcupine) object, and monitors the audio
         stream for occurrences of the wake word(s). It prints the time of detection for each occurrence and index of
         wake word.
         """

        num_keywords = len(self._keyword_file_paths)

        keyword_names = \
            [os.path.basename(x).replace('.ppn', '').replace('_tiny', '').split('_')[0] for x in
             self._keyword_file_paths]

        print('listening for: "friday"')
        #for keyword_name, sensitivity in zip(keyword_names, sensitivities):
        #    print('- %s (sensitivity: %f)' % (keyword_name, sensitivity))

        porcupine = None
        pa = None
        audio_stream = None
        try:
            porcupine = Porcupine(
                library_path=self._library_path,
                model_file_path=self._model_file_path,
                keyword_file_paths=self._keyword_file_paths,
                sensitivities=self._sensitivities)

            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length,
                input_device_index=self._input_device_index)

            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                if self._output_path is not None:
                    self._recorded_frames.append(pcm)

                result = porcupine.process(pcm)
                if num_keywords == 1 and result:                                 #######WORD DETECTED
                    print('[%s] detected keyword' % str(datetime.now()))
                    #playbeep()


                    #speechrec.startdetection()

                    p = multiprocessing.Process(target=speechrec.startdetection())
                    p.start()

                    # Wait for 10 seconds or until process finishes
                    p.join(2)

                    # If thread is still active
                    if p.is_alive() and audresp.speechtext=="":
                        print("running... let's kill it...")

                        # Terminate
                        p.terminate()
                        p.join()

                elif num_keywords > 1 and result >= 0:
                    print('[%s] detected %s' % (str(datetime.now()), keyword_names[result]))

        except KeyboardInterrupt:
            print('stopping ...')
        finally:
            if porcupine is not None:
                porcupine.delete()

            if audio_stream is not None:
                audio_stream.close()

            if pa is not None:
                pa.terminate()

            if self._output_path is not None and len(self._recorded_frames) > 0:
                recorded_audio = np.concatenate(self._recorded_frames, axis=0).astype(np.int16)
                soundfile.write(self._output_path, recorded_audio, samplerate=porcupine.sample_rate, subtype='PCM_16')

    _AUDIO_DEVICE_INFO_KEYS = ['index', 'name', 'defaultSampleRate', 'maxInputChannels']

    @classmethod
    def show_audio_devices_info(cls):
        """ Provides information regarding different audio devices available. """

        pa = pyaudio.PyAudio()

        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            print(', '.join("'%s': '%s'" % (k, str(info[k])) for k in cls._AUDIO_DEVICE_INFO_KEYS))

        pa.terminate()

def _default_library_path():
    system = platform.system()
    machine = platform.machine()

    if system == 'Darwin':
        return os.path.join(os.path.dirname(__file__), 'lib/mac/%s/libpv_porcupine.dylib' % machine)
    elif system == 'Linux':
        if machine == 'x86_64' or machine == 'i386':
            return os.path.join(os.path.dirname(__file__), '.lib/linux/%s/libpv_porcupine.so' % machine)
        else:
            raise Exception(
                'cannot autodetect the binary type. Please enter the path to the shared object using --library_path command line argument.')
    elif system == 'Windows':
        if platform.architecture()[0] == '32bit':
            return os.path.join(os.path.dirname(__file__), 'lib\\windows\\i686\\libpv_porcupine.dll')
        else:
            return os.path.join(os.path.dirname(__file__), 'lib\\windows\\amd64\\libpv_porcupine.dll')
    raise NotImplementedError('Porcupine is not supported on %s/%s yet!' % (system, machine))


def playbeep():


    wave_obj = sa.WaveObject.from_wave_file("focusbeep.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

class Audioresponse():

    def __init__(self):
        self.speechtext=""
        self.flags=[]
        self.currenciesinspeech=[]
        self.nodes=[]
        self.verbs=[]
        self.vals=[]
        self.numbers=[]
        self.contextdata=[]

class AudioRecognition(Thread):

    def __init__(self):
        Thread.__init__(self)

    def startcontextereset(self):
        if len(contextresettimers) == 0:
            contextresettimers.append(ContextResetTimer())
            contextresettimers[0].start()

    def handleinput(self):                   ###stop face animation b4 returning       ###analyse speech and detect elements relavant to filters, these elemenrs are appended to resp obj as are filters
        global audresp

        speech=audresp.speechtext.replace("+","plus").lower()

        response=None
        eel.yousaid(speech)

        cancellist=["shut up","cancel","stop listening"]
        currency=["£","$","bitcoin","litecoin","dollars","pounds"]
        if any(ext in speech for ext in cancellist):
            eel.fridaysaid("cancelling")
            return

        if "opendirfilechoice" in audresp.flags:
            if "download" in audresp.speechtext:            ##if download and a number in speech interpret as download instruction
                print("download ing")
                eel.fridaysaid("ok sending link to jDownloader or something lol")

                ###TODO follow up file selection, link to J downloader?
                audresp=Audioresponse()
                eel.stoplistening()

                return
            else:
                eel.fridaysaid("Would you like to select a file?")
                longest=0
                for file in audresp.contextdata[0]:
                    if len(file["name"])>longest:
                        longest=len(file["name"])
                for file in audresp.contextdata[0]:
                    name = file["name"]
                    #print(f"{name:<{longest}}",file["url"])

                speechrec.startdetection()

            return

        if "clear context" in audresp.speechtext:
            audresp=Audioresponse()
            eel.stoplistening()
            return

        if "scan for nodes" in audresp.speechtext:
            nodeman.scanfornodes()
            eel.stoplistening()
            return

        if "what" in audresp.speechtext and "temperature" in audresp.speechtext:
            Webfunctions().gettemp()
            eel.stoplistening()
            return

        ###currency convertion

        currencycount=0
        currenciesinspeech=[]
        for str in currency:
            if str in speech:
                currenciesinspeech.append(str)
                currencycount+=1
        if currencycount==2 and any(char.isdigit() for char in speech):             #there are two currencies and a number

            #audresp.flags.append("currencyconversion")
            audresp.currenciesinspeech=currenciesinspeech
            speech=speech.replace("£","").replace("$","")
            numbers = []
            for t in speech.split():                #TODO replace with regex and do earlier
                try:
                    t = t.replace(",", "")
                    numbers.append(float(t))
                except ValueError:
                    pass
            audresp.numbers = numbers
            if len(numbers)==1:
                print("converting",numbers[0],"from",currenciesinspeech[0],"to",currenciesinspeech[1])
                newamount = Webfunctions().currencyconverter()
                print(newamount)
                eel.fridaysaid(newamount)
            else:

                eel.fridaysaid("error finding conversion amount")
                print("too many or not enough numbers in input")
            eel.stoplistening()
            audresp=Audioresponse()
            return


        ######## Open Directory Search

        if "open directories" in speech and "search" in speech:
            pass
            if "for" in speech:
                term=speech[speech.index("for")+3:]
                if len(term)>3:
                    Webfunctions().opendirsearch(term)
                    self.startcontextereset()







        for node in nodeman.nodelist:
            if any(verb in speech for verb in node.verblist) and any(val in speech for val in node.verblist) and node.name in speech:     ###if speech contains a node name and one of its verbs and one of its verbs
                #audresp.flags.append("nodecommand")


                for verb in node.verblist:  ##find which verb it was                    ##detect elements
                    if verb in speech:
                        selectedverb=verb
                        break
                for val in node.vallist:    ##find val it was
                    if val in speech:
                        selectedvalue=val
                        break

                audresp.verbs.append(selectedvalue)                                     ##append to audio response object
                audresp.nodes.append(node)
                audresp.vals.append(selectedvalue)
                print("ayy u talking about",node.name,"and u tryna",selectedverb,selectedvalue)

                eel.stoplistening()
                nodeman.send(node.name,selectedverb,selectedvalue)
                return


        ####resolution####I think ideally the above would be filters that act on the audioResponse obj the above below
        ##would choose from the possible options that the characteristics of the input would allow


        print("audio response handler closing")
        eel.stoplistening()
        eel.fridaysaid(response)

    def startdetection(self):
        global audresp,detector
        audresp.speechtext=""
        try:
            detector.terminate() ###for snowboy
        except Exception:
            pass
        inconvo=True
        r = speech_rec.Recognizer()
        with speech_rec.Microphone() as source:
            print("Listening")
            eel.showlistening()
            audio = r.listen(source,timeout=5,phrase_time_limit=10) ##sometimes this runs forever


        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            speech=r.recognize_google(audio)
            print("\"" + speech+"\"")
            audresp.speechtext=speech
            self.handleinput()

        except speech_rec.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            inconvo=False
            eel.stoplistening()
            eel.yousaid("Couldnt understand audio")
        except speech_rec.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            inconvo=False
        try:
            detector.start(AudioRecognition().startdetection)       ###for snowboy
        except Exception:
            pass



class GUIstartClass(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        eel.init('web')

        try:
            # options = {
            #     'mode': 'custom',
            #     'args': ['node_modules/electron/dist/electron.exe', '.']
            # }
            options = {
                'mode': 'chrome',
                "args":["--kiosk --fullscreen --chromeframe"]

            }
            start_urls="main.html"
            #eel.start(start_urls='main.html',options=options)

            eel.start("main.html",options=options)
        except (SystemExit, MemoryError, KeyboardInterrupt):
            # We can do something here if needed
            # But if we don't catch these safely, the script will crash
            pass
        print("GUI closed")

#TODO add spotify on display
## and voice commands ofc :P

class GUITHREAD(Thread):
    global inconvo
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        pass
        #eel.sleep(4)


class ContextResetTimer(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global audresp
        print("context reset started")
        time.sleep(30)
        print("context resetting")
        audresp=Audioresponse()

class NodeManager(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.nodelist=[]

    def setupgrammar(self):
        root = ET.parse('Nodes.xml').getroot()
        for child in root.iter("Node"):
            name=child.find("FName").text
            mac=child.find("Mac").text
            ip=child.find("IP").text
            verbs=child.find("Verbs").text.split(",")
            vals=child.find("Vals").text.split(",")
            self.nodelist.append(Node(name,mac,ip,verbs,vals))

    def scanfornodes(self):
        #for node in nodeman.nodelist:
        #    node.online=False

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip=s.getsockname()[0]

        ##TODO programatically get subnet mask
        subnet="255.255.255.0"

        ipwithmask=str(IPNetwork(ip+"/"+subnet).cidr)

        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ipwithmask), timeout=4)

        #print(ans.summary())
        macs=[]
        for device in ans.res:
            mac=device[1].payload.hwsrc
            ip=device[1].payload.fields["psrc"]
            print(mac)
            macs.append({"mac":mac,"ip":ip})
            for node in self.nodelist:
                if mac.lower() == node.mac.lower():
                    node.online=True
                    node.ip=ip
                    print(node.name,"node is online")




    def send(self,Fname,verb,value):
        for node in self.nodelist:
            if node.name==Fname:
                if node.online or node.ip!="":
                    try:
                        url="http://" + node.ip + "/" + verb + "/" + value
                        print("getting",url)
                        #eel.fridaysaid("GET http://"+url)
                        r = requests.get(url=url)
                        print(r)
                        if r.status_code==200:
                            eel.fridaysaid("Done")
                    except Exception:
                        print("timeout on", self.ip)
                        eel.fridaysaid("node timed out")
                    break
                else:
                    eel.fridaysaid("node offline")
                    print("node offline")

class Node():

    def __init__(self,name,mac,ip,verblist,vallist):
        self.name=name
        self.mac=mac
        self.ip=ip
        self.verblist=verblist
        self.vallist=vallist
        self.online=None



class Webfunctions():

    def __init__(self):
        pass

    def getlocation(self):
        global latlong
        g = geocoder.ipinfo('me')
        latlong=g.latlng
        data={}
        data["lat"]=latlong[0]
        data["long"]=latlong[1]
        data["city"]=g.current_result.city
        with open('web/location.json', 'w') as outfile:
            json.dump(data, outfile)

    def getisspassoverjson(self):
        global latlong
        if latlong==None:
            self.getlocation()

        try:
            response = requests.get("http://api.open-notify.org/iss-pass.json?n=100&lat=+"+str(latlong[0])+"&lon="+str(latlong[1]))

            # If the response was successful, no Exception will be raised
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print(response.text)
            with open('web/iss.json', 'w') as outfile:
                json.dump(response.json(), outfile)




    def gettemp(self):
        if latlong==None:
            self.getlocation()

        #TODO move api key into seperate file
        openweatherapikey="77d556c4a3afa89eb1b61a0a836a40c6"
        #url=f"https://api.openweathermap.org/data/2.5/weather?lat={latlong[0]}&lon={latlong[1]}&units=metric&appid={openweatherapikey}"
        url="https://api.openweathermap.org/data/2.5/weather?lat="+str(latlong[0])+"&lon="+str(latlong[1])+"&units=metric&appid="+openweatherapikey
        print(url)
        resp = requests.get(url=url)
        data = resp.json()
        temp=data["main"]["temp"]
        print("current temp is",temp,"degrees")
        eel.fridaysaid("it is "+str(temp)+" degrees")


    def currencyconverter(self):
        global audresp
        currency1 = audresp.currenciesinspeech[0].replace("£", "GBP").replace("$", "USD").replace("dollars",
                                                                                                  "USD").replace(
            "pounds", "GBP")
        currency2 = audresp.currenciesinspeech[1].replace("£", "GBP").replace("$", "USD").replace("dollars",
                                                                                                  "USD").replace(
            "pounds", "GBP")
        amount = audresp.numbers[0]
        crypto = ["bitcoin", "litcoin"]
        if currency2 == "bitcoin":
            b = BtcConverter()
            return str(b.convert_to_btc(amount, currency1)) + " btc"
        else:
            c = CurrencyRates()
            convertion = c.convert(currency1, currency2, amount)
            return currency2.replace("GBP", "£").replace("USD", "$") + str(convertion)


    def opendirsearch(self,term):
        eel.stoplistening()
        #TODO loading animation
        browser.set_page_load_timeout(20)
        originalterm=term
        term=term.strip()


        filetypes = [".mp4", ".mkv"]

        url="https://www.google.com/search?q=+intext:"+term+"%20intitle:%22index.of%22%20-inurl:(jsp|pl|php|html|aspx|htm|cf|shtml)"

        browser.get(url)
        #print(browser.page_source)

        validlinks=[]
        links = browser.find_elements_by_tag_name("a")
        for link in links:
            url=link.get_attribute("href")
            if "/url?q" in url and "accounts.google" not in url:
                url=url.replace("https://www.google.com/url?q=","")
                url=url[:url.index("&sa=")]
                url=url.replace("%25","%")
                if "google.com" not in url:
                    validlinks.append(url)

        print(validlinks)
        eel.fridaysaid("Searching... "+str(len(validlinks))+" sources")
        eel.makeprogressbar()
        files=[]
        count=1
        for link in validlinks:
            if count==10:
                break
            print("link",count,"out of ",str(len(validlinks)))
            eel.setprogressbar(count/len(validlinks))
            try:
                browser.get(link)
                filelinks= browser.find_elements_by_tag_name("a")
                for filelink in filelinks:
                    ###ignore the pareent directory links an shit
                    url = filelink.get_attribute("href")
                    if "/" in url[-1:]:
                        continue

                    if any(ext in url[-4:] for ext in filetypes):

                        origterms = originalterm.lower().split()
                        if all(term in url.lower() for term in origterms):   ##if the search terms are in the filename
                            urlparts=url.split("/")
                            name=urlparts[len(urlparts)-1]
                            name=name.replace("%5d","]").replace("%5b","[").replace("%20"," ")
                            files.append({"name":name,"url":url})
                            print("got",str(len(files)),"files")

            except Exception:
                print("page probably failed to load or timed out")
            count+=1
        print("Got "+str(len(files))+" matching links")
        eel.fridaysaid("Got "+str(len(files))+" matching links")
        eel.stoplistening()


        if len(files)>0:
            audresp.flags.append("opendirfilechoice")
            audresp.contextdata.append(files)
            speechrec.handleinput()


def startporcupine():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword_file_paths', help='comma-separated absolute paths to keyword files', type=str)
    parser.add_argument(
        '--library_path',
        help="absolute path to Porcupine's dynamic library",
        type=str)

    parser.add_argument(
        '--model_file_path',
        help='absolute path to model parameter file',
        type=str,
        default=os.path.join(os.path.dirname(__file__), 'lib/common/porcupine_params.pv'))

    parser.add_argument('--sensitivities', help='detection sensitivity [0, 1]', default=0.5)
    parser.add_argument('--input_audio_device_index', help='index of input audio device', type=int, default=None)

    parser.add_argument(
        '--output_path',
        help='absolute path to where recorded audio will be stored. If not set, it will be bypassed.',
        type=str,
        default=None)

    parser.add_argument('--show_audio_devices_info', action='store_true')

    args = parser.parse_args()


    if args.show_audio_devices_info:
        PorcupineDemo.show_audio_devices_info()
    else:
        if not args.keyword_file_paths:
            args.keyword_file_paths = "friday_windows.ppn"  ######HERE IS SOME HARDCODING SO THE PY CAN BE RUN FROM THE IDE
            # raise ValueError('keyword file paths are missing')

        keyword_file_paths = [x.strip() for x in args.keyword_file_paths.split(',')]

        if isinstance(args.sensitivities, float):
            sensitivities = [args.sensitivities] * len(keyword_file_paths)
        else:
            sensitivities = [float(x) for x in args.sensitivities.split(',')]

        PorcupineDemo(
            library_path=args.library_path if args.library_path is not None else _default_library_path(),
            model_file_path=args.model_file_path,
            keyword_file_paths=keyword_file_paths,
            sensitivities=sensitivities,
            output_path=args.output_path,
            input_device_index=args.input_audio_device_index).run()



if __name__ == '__main__':

    startgui = GUIstartClass()
    startgui.start()
    guithread=GUITHREAD()
    guithread.start()
    speechrec=AudioRecognition()
    nodeman = NodeManager()
    nodeman.setupgrammar()
    audresp = Audioresponse()

    Webfunctions().getlocation()
    Webfunctions().getisspassoverjson()


    nodeman.scanfornodes()


    # chrome_options = Options()
    # #chrome_options.add_argument("headless")
    # chrome_options.add_argument("--window-size=20,20")
    # chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})
    # chrome_options.add_argument(
    #     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36")
    # chrome_options.add_argument("--disable-javascript")
    # browser = Chrome(chrome_options=chrome_options)

    eel.showlineanimation()
    try:                            ###for linux/rpi
        detector = snowboydecoder.HotwordDetector("Friday.pmdl", sensitivity=0.48, audio_gain=8)
        detector.start(AudioRecognition().startdetection)       ##WORD DETECTED
    except Exception:               ###for windows
        startporcupine()






#TODO hardware button to trigger voice recognition
